import matlab.engine

eng = matlab.engine.start_matlab()

# To import a function from a hurst_wavelet_mf.m file, use the following:
eng.addpath(r'C:\Users\zuire\PycharmProjects\pythonProject1\Propofol\hurst_wavelet_mf.m', nargout=0)
eng.hurst_wavelet_mf(nargout=0)

