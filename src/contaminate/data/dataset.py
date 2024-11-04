import random
import pandas as pd
import torch
from typing import Optional
import ir_datasets as irds
from torch.utils.data import Dataset
from rankers._util import load_json

MSMARCO_TRIPLES = r'msmarco-passage/train/triples-small'
DL19 = r"msmarco-passage/trec-dl-2019/judged"
DL20 = r"msmarco-passage/trec-dl-2020/judged"
COVID = r"beir/trec-covid"

class TrainingDataset(Dataset):
    def __init__(self, 
                 training_data : pd.DataFrame, 
                 teacher_file : Optional[str] = None,
                 group_size : int = 2,
                 listwise : bool = False,
                 covid : bool = False
                 ) -> None:
        super().__init__()
        self.training_data = training_data
        self.teacher_file = teacher_file
        self.group_size = group_size
        self.listwise = listwise
        self.covid = covid

        self.__post_init__()

    
    def __post_init__(self):
        msmarco = irds.load(MSMARCO_TRIPLES)
        dl19 = irds.load(DL19)
        dl20 = irds.load(DL20)
        if self.covid: covid = irds.load(COVID)
        for column in 'query_id', 'doc_id_a', 'doc_id_b':
            if column not in self.training_data.columns: raise ValueError(f"Format not recognised, Column '{column}' not found in triples dataframe")
        self.docs = pd.DataFrame(msmarco.docs_iter()).set_index("doc_id")["text"].to_dict()
        if self.covid: self.docs.update(pd.DataFrame(covid.docs_iter()).set_index("doc_id")["text"].to_dict())
        msmarco_queries = pd.DataFrame(msmarco.queries_iter()).set_index("query_id")["text"].to_dict()
        dl19_queries = pd.DataFrame(dl19.queries_iter()).set_index("query_id")["text"].to_dict()
        dl20_queries = pd.DataFrame(dl20.queries_iter()).set_index("query_id")["text"].to_dict()

        self.queries = {**msmarco_queries, **dl19_queries, **dl20_queries}
        if self.covid: self.queries.update(pd.DataFrame(covid.queries_iter()).set_index("query_id")["text"].to_dict())

        if self.teacher_file: self.teacher = load_json(self.teacher_file)

        self.labels = True if self.teacher_file else False
        self.multi_negatives = True if type(self.training_data['doc_id_b'].iloc[0]) == list else False

        if not self.listwise:
            if self.group_size > 2 and self.multi_negatives:
                self.training_data['doc_id_b'] = self.training_data['doc_id_b'].map(lambda x: random.sample(x, self.group_size-1))
            elif self.group_size == 2 and self.multi_negatives:
                self.training_data['doc_id_b'] = self.training_data['doc_id_b'].map(lambda x: random.choice(x))
                self.multi_negatives = False
            elif self.group_size > 2 and not self.multi_negatives:
                raise ValueError("Group size > 2 not supported for single negative samples")
    
    def __len__(self):
        return len(self.training_data)
    
    def _teacher(self, qid, doc_id, positive=False):
        assert self.labels, "No teacher file provided"
        try: return self.teacher[str(qid)][str(doc_id)] 
        except KeyError: return 0.

    def __getitem__(self, idx):
        item = self.training_data.iloc[idx]
        qid, doc_id_a, doc_id_b = item['query_id'], item['doc_id_a'], item['doc_id_b']
        query = self.queries[str(qid)]
        texts = [self.docs[str(doc_id_a)]] if not self.listwise else []

        if self.multi_negatives: texts.extend([self.docs[str(doc)] for doc in doc_id_b])
        else: texts.append(self.docs[str(doc_id_b)])

        if self.labels:
            scores = [self._teacher(str(qid), str(doc_id_a), positive=True)] if not self.listwise else []
            if self.multi_negatives: scores.extend([self._teacher(qid, str(doc)) for doc in doc_id_b])
            else: scores.append(self._teacher(str(qid), str(doc_id_b)))
            return (query, texts, scores)
        else:
            return (query, texts)