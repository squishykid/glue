from multiprocessing import Process
import signal


def inside(param):
    from util import runtime
    runtime.enter(param)


if __name__ == '__main__':
    actors = ['actor.echo', 'actor.http', 'actor.web', 'actor.web']
    processes = []
    for actor in actors:
        p = Process(target=inside, args=(actor,))
        processes.append(p)
        p.start()
    print('waiting for ctrl-c')
    signal.sigwait([signal.SIGINT])
    for process in processes:
        process.kill()
