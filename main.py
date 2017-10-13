from multiprocessing import Process
import os
import logging
import prediction
import mega_pi_integrated
import client

def prediction_process():
	prediction.main_loop()

def write_data_process():
	#call write data function
	client.createClient('172.17.105.245',8888)
	pass

def mega_process():
	mega_pi_integrated.start_running()

if __name__ == '__main__':
	LOG_FILENAME = '/home/hazmei/Documents/git/CG3002/Integration/bballiPi.log'

	logger = logging.getLogger(__name__)
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename=LOG_FILENAME,level=logging.INFO)
	logger.setLevel(logging.DEBUG)
	#logging.getLogger('tensorflow').setLevel(logging.CRITICAL)
	logger.info('Starting {}'.format(__file__))

	#supress debugging output
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

	jobs = []

	try: 
		p = Process(target=prediction_process)
		jobs.append(p)
		p.start()

		p = Process(target=write_data_process)
		jobs.append(p)
		p.start()

		p = Process(target=mega_process)
		jobs.append(p)
		p.start()

		for proc in jobs:
			proc.join()
	except Exception as e:
		logger.critical('Exception occur: {}'.format(e))
	finally:
		logger.info('Exiting process {}'.format(__file__))
