import json
from utils.utils import *



from dataclasses import dataclass, asdict


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
    def __init__(self,name="空流水线"):
        self.name=name
        self.pipeline = []

    def gregister_pipline(self):
        _id=md5(self.name)
        item={
            'name':self.name,
            'pipeline':self.output_pipeline(),
        }
        
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
    

    # 可以运行环节的状态函数吗?  就判断一个条件 前一个必须是ok 这也是写代码常犯的错误  不自觉或者状态多了以后就开始冲突了
    # 一次就判断一个东西  自己已经完成
    def can_run_stage_func(self, stage:Stage):
        for index,one_stage in enumerate(self.pipeline):
            if one_stage.name != stage.name:
                continue
            if index == 0 :
                return True
            if one_stage.step == 'ok':
                logger.info("当前环节已经ok 完成,不会再次进入主逻辑了")
                return False
            
            pre_stage=self.pipeline[index-1]
            if pre_stage.step != 'ok':
                logger.info("上一个环节未完成")
                return False
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









