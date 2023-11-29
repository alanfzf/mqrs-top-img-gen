if (-Not (Test-Path -Path "./env/")) {
    py -m venv env 
    ./env/Scripts/Activate
    pip install -r req.txt
}else{
  ./env/Scripts/Activate
} 

py main.py
