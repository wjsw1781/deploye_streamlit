import json
from utils.utils import *



from dataclasses import dataclass, asdict

from pymongo import MongoClient
import redis 
#mongodb://root:1213wzwz@139.196.158.152:27017/admin

table_name='pipline_tasks'

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

db = client.zhiqiang_hot
table=db[table_name]


@dataclass
class Stage:
    name: str
    step: str = "pending"
    error: bool = False
    desc:str="无描述"
    @classmethod
    def from_dict(cls, **data):
        return cls(**data)


class pipeline:
    def __init__(self,name):
        self.name=name
        self.pipeline = []

    def gregister_pipline(self):
        _id=md5(self.name)
        item={
            'name':self.name,
            'pipeline':self.output_pipeline(),
        }
        table.update_one({'_id':_id},{'$set':item},upsert=True)
        
    def add_stage(self, stage):
        self.pipeline.append(stage)
        if len(self.pipeline)==1:
            self.pipeline[0].step = 'ok'
        self.gregister_pipline()


    # 修改状态
    def change_stage_step_ok(self,stage:Stage):
        for index,one_stage in enumerate(self.pipeline):
            if one_stage.name == stage.name:

                pre_stage=index-1
                if pre_stage>=0:
                    if self.pipeline[pre_stage].step != 'ok':
                        raise ValueError("上一个环节未完成")

                one_stage.step = 'ok'
                next_stage=index+1
                
                if len(self.pipeline)>next_stage:
                    self.pipeline[next_stage].step = 'running'

    def change_stage_step_error(self,stage:Stage,error_info):
        for index,one_stage in enumerate(self.pipeline):
            if one_stage.name == stage.name:
                one_stage.step ='error'
                one_stage.error =error_info

                

    def restore_pipeline(self,data):
        self.pipeline=[]
        for stage in json.loads(data):
            self.pipeline.append(Stage.from_dict(**stage))
        return self

    def output_pipeline(self):
        dict_list=[asdict(stage) for stage in self.pipeline]
        return json.dumps(dict_list,ensure_ascii=False)
    

    # 可以运行环节的状态函数吗?
    def can_run_stage_func(self, stage:Stage):
        for index,one_stage in enumerate(self.pipeline):
            if index == 0:
                return True
            pre_stage=self.pipeline[index-1]
            if one_stage.name == stage.name and one_stage.step == 'pending' and pre_stage.step=='ok' :
                return True
        return False


    # 可视化方式展示 所有环节的状态
    def get_gradio_compent(self):
        pass
    
    def get_html_compent(self):
        pass

if __name__ == '__main__':
    
    pipeline_obj = pipeline(name="测试流水线总表")
    stage_obj1 = Stage('1')
    stage_obj2 = Stage('2')
    stage_obj3 = Stage('3')
    stage_obj4 = Stage('4')
    pipeline_obj.add_stage(stage_obj1)
    pipeline_obj.add_stage(stage_obj2)
    pipeline_obj.add_stage(stage_obj3)
    pipeline_obj.add_stage(stage_obj4)

    print(pipeline_obj.output_pipeline())
    
    pipeline_obj.restore_pipeline(pipeline_obj.output_pipeline())

    print(pipeline_obj.output_pipeline())
    
    stage_obj1.step = 'ok'
    pipeline_obj.change_stage_step_ok(stage_obj1)
    print(pipeline_obj.output_pipeline())
    
    stage_obj2.step = 'ok'
    pipeline_obj.change_stage_step_ok(stage_obj2)
    print(pipeline_obj.output_pipeline())
    
    stage_obj3.step = 'ok'
    pipeline_obj.change_stage_step_ok(stage_obj3)
    print(pipeline_obj.output_pipeline())
    
    stage_obj4.step = 'ok'
    pipeline_obj.change_stage_step_ok(stage_obj4)
    print(pipeline_obj.output_pipeline())









