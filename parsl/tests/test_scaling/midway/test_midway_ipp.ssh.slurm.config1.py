from parsl import *
import parsl
import libsubmit

parsl.set_stream_logger()
print(parsl.__version__)
print(libsubmit.__version__)

MIDWAY_USERNAME = "yadunand"
config = {
    "sites" : [
        { "site" : "Local_IPP",
          "auth" : {
              "channel" : "ssh",
              "hostname" : "swift.rcc.uchicago.edu",
              "username" : MIDWAY_USERNAME,
              "scriptDir" : "/scratch/midway2/{0}/parsl_scripts".format(MIDWAY_USERNAME)
          },
          "execution" : {
              "executor" : "ipp",
              "provider" : "slurm",
              "block" : {                  # Definition of a block
                  "nodes" : 1,             # of nodes in that block
                  "taskBlocks" : "$CORES", # total tasks in a block
                  "walltime" : "00:05:00",
                  "initBlocks" : 1,
                  "maxBlocks" : 1,
                  "options" : {
                      "partition" : "westmere",
                      "overrides" : '''module load python/3.5.2+gcc-4.8; source /scratch/midway2/yadunand/parsl_env_3.5.2_gcc/bin/activate'''
                  }
              }
          }
        }
        ],
    "globals" : {   "lazyErrors" : True },
    #"controller" : { "publicIp" : '*' }
}

dfk = DataFlowKernel(config=config)


@App("python", dfk)
def python_app():
    import platform
    return "Hello from {0}".format(platform.uname())


@App("bash", dfk)
def bash_app(stdout=None, stderr=None):
    return 'echo "Hello from $(uname -a)" ; sleep 2'


def test_python(N=100):
    import os
    results = {}
    for i in range(0,N):
        results[i] = python_app()

    print("Waiting ....")
    print(results[0].result())


def test_bash():
    import os
    fname = os.path.basename(__file__)

    x = bash_app(stdout="{0}.out".format(fname))
    print("Waiting ....")
    print(x.result())


if __name__ == "__main__" :

    test_python()
    #test_bash()
