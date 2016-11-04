import concurrent.futures


def process_with_threadpool(obj_list, func, max_workers=2):
    """
    Some tasks can take long time, like running a list with API calls. 
    Using a Threadpool you can speed that up alot!
    @param obj_list: list of object to run func on
    @param func: function to do on obj_list
    @param max_workers: how much conurrency? be careful, to high can make host
    unresponsive.
    """
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        result = {executor.submit(func, o): o for o in obj_list}
