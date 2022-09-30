from .data_utils import load_widefield_raw, load_widefield_SVD

class Widefield():
    def __init__(self,Session):
        self.alVc = None
        self.segFrames = None
        self.segInx = None
        self.transParams = None
        self.raw = load_widefield_raw(Session.paths['wfield'])
        self.U, self.Vc = load_widefield_SVD(Session.paths['svd'])