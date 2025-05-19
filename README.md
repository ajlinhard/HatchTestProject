# HatchTestProject
building bare bones web message API


## Assumptions
- The send messages are only coming from Hatch/Hatch Clients to their customers.
- The receive messages are only coming from customers.

## To Run:
1. install the project using the msgapp-env.yml
```bash
conda env create -f msgapp-env.yml
```
2. Activate the environment

3. Then go to the directory via cd, and call the app
```bash
python -m src.MessageService
```

4. Send test request, examples in tests\Test_Message_Sending.ipynb