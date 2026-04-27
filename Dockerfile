FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 120 --retries 3 -r requirements.txt \
    && pip uninstall -y nvidia-nccl-cu12 nvidia-cublas-cu12 nvidia-cuda-runtime-cu12 \
       nvidia-cuda-cupti-cu12 nvidia-cuda-nvrtc-cu12 nvidia-cudnn-cu12 \
       nvidia-cufft-cu12 nvidia-curand-cu12 nvidia-cusolver-cu12 \
       nvidia-cusparse-cu12 nvidia-nvjitlink-cu12 nvidia-nvtx-cu12 2>/dev/null; \
    true

COPY . .

RUN python run_all.py

EXPOSE 8501

CMD ["streamlit", "run", "demo/app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--browser.gatherUsageStats", "false"]
