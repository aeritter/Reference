# This can be used to watch a folder and only continue when a change has happened within the folder (file added, changed, deleted, etc)
# By using the Windows API, we can watch the folder and wait for it to notify us that a change has happened rather than polling it and comparing the current state to the previous state
# Using the Windows API, we can also set a timeout so it can do stuff in the meantime if no changes have been found (such as cleanup or checking in with another service)

import win32file, win32con, win32event, pywintypes

def main():
    flags = win32con.FILE_NOTIFY_CHANGE_FILE_NAME
    dh = win32file.CreateFile("C:\\", 0x0001,win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS | win32con.FILE_FLAG_OVERLAPPED, None)
    overlapped = pywintypes.OVERLAPPED()
    overlapped.hEvent = win32event.CreateEvent(None, 0, 0, None)
    buf = win32file.AllocateReadBuffer(8192)

    changes = []
    iterations = 0
    timedout = False

    while True:
        iterations+=1
        print(iterations)

        if timedout == False:        # This is to ensure the directory handle only has one instance of ReadDirectoryChangesW at a time.
                                # If this isn't here and ReadDirectoryChangesW stacks up without being used, it will break after 60-64 iterations if
                                # using a mapped network folder and the directory handle will need to be closed (dh.close()) and reopened.
            win32file.ReadDirectoryChangesW(dh, buf, True, flags, overlapped)

        rc = win32event.MsgWaitForMultipleObjects([overlapped.hEvent], False, 5000, win32event.QS_ALLEVENTS)
        # rc = win32event.WaitForSingleObject(overlapped.hEvent, 5000)                  # Also acceptable
        # rc = win32event.WaitForMultipleObjects([overlapped.hEvent], False, 5000)      # Also acceptable
        if rc == win32event.WAIT_TIMEOUT:
            timedout = True
            print('timed out')
        if rc == win32event.WAIT_OBJECT_0:      # can replace win32event.WAIT_OBJECT_0 with the integer 0 (and win32event.WAIT_OBJECT_0+1 with 1)
            timedout = False        # since we got a result, reset the timedout variable so ReadDirectoryChangesW can be run again
            result = win32file.GetOverlappedResult(dh, overlapped, True)
            if result:
                bufferData = win32file.FILE_NOTIFY_INFORMATION(buf, result)
                changes.extend(bufferData)
                print(bufferData)
                for x in bufferData:
                    if x[1] == 'break':         # for testing, create a file named "break" in the watched folder and the script will stop and print the list of files
                        print("\nFinal result!")
                        return changes
            else:
                print('dir handle closed')
        # elif rc == win32event.WAIT_OBJECT_0+1:
        #     do stuff here if there's a second object that can trigger rc


        # if iterations >= 59:      # this section only needed if the timedout stuff above is not added. Prefer the above usage. This is only for reference.
        #     iterations = 0
        #     dh.close()
        #     dh = win32file.CreateFile("Z:\\", 0x0001,win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS | win32con.FILE_FLAG_OVERLAPPED, None)


for x, filename in main():
    print(x, filename)
