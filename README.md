##Jiani
###Environment
To execute this code you just need to install Anaconda or Conda in your system, then execute pip install -r requirement.txt.
###Baseline model outputs
First, run the **DeepSimulator** code to get the baseline generated event log, as well as the embedding matrix of the activities.
Since we use the same generated arrival times for each trace as the DeepSimulator and the embedding matrix to compute the nearest activities, we need the output of the baseline model.

(In the directory `example_datasets`, we already have the outputs of DeepSimulator with some datasets.)

###Our method
* In our method, generate the sequence of trace activities first. All generated logs are saved in the directory `example_outputs`.   
example:

`python scripts\log_gen_seq.py --experiment-name "ConsultaDataMining201618_0.2" --import-file "example_datasets\ConsultaDataMining201618_0.2\train_ConsultaDataMining201618.xes" --import-test-file "example_datasets\ConsultaDataMining201618_0.2\test_ConsultaDataMining201618.xes" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition" --method prefix
`

* Then, generate the time of each activity, both start time and end time.  
example:

`python scripts\log_gen_time.py --experiment-name "ConsultaDataMining201618_0.2" --import-file "example_datasets\ConsultaDataMining201618_0.2\train_ConsultaDataMining201618.xes" --simulator-output "example_datasets\ConsultaDataMining201618_0.2\gen_ConsultaDataMining201618_1.csv" --embedding-matrix "example_datasets\ConsultaDataMining201618_0.2\embedded_matix\ac_DP_ConsultaDataMining201618.emb" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition"
`

* Finally, generate the resource of each activity.  
example:

`python scripts\log_gen_res.py --experiment-name "ConsultaDataMining201618_0.2" --import-file "example_datasets\ConsultaDataMining201618_0.2\train_ConsultaDataMining201618.xes" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition"
`

parameters explanations:

`--experiment-name` : the name of experiment  
`--import-file` : train file(xes file in our case)  
`--import-test-file` : test file(xes file in our case)   
`--id-column` : name of 'case id' factor  
`--act-column` : name of 'activity' factor  
`--time-column` : name of 'timestamp' factor  
`--resource-column` : name of 'resource' factor  
`--state-column` : name of 'state'(state can be start or complete in xes file) factor  
`--method` : sequence generation method: prefix or n-gram  
`--num` : n of n-gram  
`--simulator-output` : generated log file from DeepSimulator  
`--embedding-matrix` : embbeding matrix file for the activities(got from the output of DeepSimulator)  


###other example datasets:  
*Production*  
* gen_seq  
`python scripts\log_gen_seq.py --experiment-name "Production_0.2" --import-file "example_datasets\Production_0.2\train_Production.xes" --import-test-file "example_datasets\Production_0.2\test_Production.xes" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition" --method prefix
`
* gen_time  
`python scripts\log_gen_time.py --experiment-name "Production_0.2" --import-file "example_datasets\Production_0.2\train_Production.xes" --simulator-output "example_datasets\Production_0.2\gen_Production_1.csv" --embedding-matrix "example_datasets\Production_0.2\embedded_matix\ac_DP_Production.emb" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition"
`
* gen_res  
`python scripts\log_gen_res.py --experiment-name "Production_0.2" --import-file "example_datasets\Production_0.2\train_Production.xes" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition"
`  

*PurchasingExample*  
* gen_seq  
`python scripts\log_gen_seq.py --experiment-name "PurchasingExample_0.5" --import-file "example_datasets\PurchasingExample_0.5\train_PurchasingExample.xes" --import-test-file "example_datasets\PurchasingExample_0.5\test_PurchasingExample.xes" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition" --method prefix
`
* gen_time  
`python scripts\log_gen_time.py --experiment-name "PurchasingExample_0.5" --import-file "example_datasets\PurchasingExample_0.5\train_PurchasingExample.xes" --simulator-output "example_datasets\PurchasingExample_0.5\gen_PurchasingExample_1.csv" --embedding-matrix "example_datasets\PurchasingExample_0.5\embedded_matix\ac_DP_PurchasingExample.emb" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition"
`
* gen_res  
`python scripts\log_gen_res.py --experiment-name "PurchasingExample_0.5" --import-file "example_datasets\PurchasingExample_0.5\train_PurchasingExample.xes" --id-column caseid --act-column "concept:name" --time-column "time:timestamp" --resource-column user --state-column "lifecycle:transition"
`

  
  

Below is the readme of *DeepSimulator*:  



# DeepSimulator: Learning Accurate Business Process Simulation Models from Event Logs via Automated Process Discovery and Deep Learning

DeepSimulator is a hybrid approach able to learn process simulation models from event logs wherein a (stochastic) process model is extracted via DDS techniques and then combined with a DL model to generate timestamped event sequences. This code can perform the next tasks:


* Training generative models using an event log as input.
* Generate full event logs using the trained generative models.
* Assess the similarity between the original log and the generated one.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

To execute this code you just need to install Anaconda or Conda in your system, then execute pip install -r requirement.txt.

## Running the script

Once created the environment, you can execute the tool from a terminal specifying the input event log name and any of the following parameters:

* `--file (required)`: event log in XES format, the event log must be previously located in the `input_files/event_logs` folder
* `--update_gen/--no-update_gen (optional, default=False)`: Refers to whether you want to update the sequences generation model previously discovered. If this parameter is added, the entire discovery pipeline will be executed. Additionally, if this parameter is set, the number of repetitions of every experiment can be configured with the parameter `--s_gen_repetitions (optional, default=5)`, and the number of experiments with `--s_gen_max_eval (optional, default=30)`.
* `--update_ia_gen/--no-update_ia_gen (optional, default=False)`: Refers to whether you want to update the inter-arrivals generation model previously discovered. If this parameter is added, the entire discovery pipeline will be executed.
* `--update_times_gen/--no-update_times_gen (optional, default=False)`: Refers to whether you want to update the deep-learning times generation models previously discovered. If this parameter is added, the entire discovery pipeline will be executed. Additionally, if this parameter is set, the number of training epochs can be configured with the parameter `--t_gen_epochs (optional, default=200)`, and the number of experiments with `--t_gen_max_eval (optional, default=12)`.
* `--save_models/--no-save_models (optional, default=True)`: Refers to whether or not you want to save the discovered models.
* `--evaluate/--no-evaluate (optional, default=True)`: Refers to whether or not you want to perform a final assessment of the accuracy of the final simulation model.
* `--mining_alg (optional, default='sm1')`: version of SplitMiner to use. Available options: 'sm1', 'sm2', 'sm3'.

**Example of basic execution:**

```shell
(deep_simulator) PS C:\DeepSimulator> python .\pipeline.py --file Production.xes
```

**Example of execution updating the deep-learning times generation models**

```shell
(deep_simulator) PS C:\DeepSimulator> python .\pipeline.py --file Production.xes --update_times_gen --t_gen_epochs 20 --t_gen_max_eval 3
```

## Examples

The datasets, models, and evaluation results can be found at <a href="https://doi.org/10.5281/zenodo.5734443" target="_blank">Zenodo</a>. The paper of the approach can be found at  <a href="https://doi.org/10.1007/978-3-031-07472-1_4" target="_blank">CAiSE'22 Paper</a>

