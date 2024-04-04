import json


class stage:
    def __init__(self, name,step="pending"):
        self.name = name
        self.step = step  # pending or running or done  or error
        self.error= False


class pipeline:
    def __init__(self):
        self.pipeline = []
        
    def add_stage(self, stage):
        self.pipeline.append(stage)
        if len(self.pipeline)==1:
            self.pipeline[0].step = 'running'

    def restore_pipeline(self,data):
        self.pipeline = json.loads(data)
    

    def output_pipeline(self):
        return json.dumps(self.pipeline,ensure_ascii=False)
    

    # 可以运行环节的状态函数吗?
    def can_run_stage_func(self, stage_name):
        for index,stage in enumerate(self.pipeline):
            if index == 0:
                continue
            pre_stage=self.pipeline[index-1]
            if stage.name == stage_name and stage.step == 'pending':
                return True
        return False


    # 可视化方式展示 所有环节的状态
    def get_gradio_compent(self):
        pass
    








