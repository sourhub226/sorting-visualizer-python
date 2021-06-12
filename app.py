from tkinter import Tk, Canvas, PhotoImage, Button, Label
from tkinter.font import Font, BOLD
import random
import time
import sys
from colour import Color

canvasbackground = "#202124"
sortSpeed = 0
no_of_pipes = 128
gap = 1
pipeWidth = 5
screenWidth = 1180 - 133
screenHeight = 522
y1Range = 512
pipeColors = list(Color("red").range_to(Color("violet"), no_of_pipes))


screen = Tk()
# screen.geometry((f"{screenWidth}x{screenHeight}"))
screen.title("Sorting Visualizer (Made by Sourabh Sathe)")
# to center the tkinter window
monitor_width = screen.winfo_screenwidth()
monitor_height = screen.winfo_screenheight()

x_cordinate = int((monitor_width - screenWidth) / 2)
y_cordinate = int((monitor_height - screenHeight) / 2)

screen.geometry(
    "{}x{}+{}-{}".format(screenWidth, screenHeight, x_cordinate, y_cordinate)
)
screen.resizable(False, False)
screen.config(bg="white")

canvasWidth = 1000 - 230
canvasHeight = screenHeight - 4
canvas = Canvas(screen, width=canvasWidth, height=canvasHeight, bg=canvasbackground)
canvas.place(x=0, y=0)
pixelVirtual = PhotoImage(width=1, height=1)


class Global:
    def __init__(self):
        self.y1CoorList = random.sample(
            range(0, y1Range, int(y1Range / no_of_pipes)), no_of_pipes
        )
        print(self.y1CoorList)
        self.sortdone = False
        self.closeWindow = False


Global = Global()
n = len(Global.y1CoorList)
print(n)


def check_sortdone():
    if Global.sortdone:
        status.config(
            text="Already Sorted. Press Shuffle.",
            foreground="#FF0000",
            font=Font(size=11, weight=BOLD),
        )
        return False
    return True


def blockBtn():
    # global btnList
    status.config(
        text="Sorting in progress",
        foreground="#FF0000",
        font=Font(size=11, weight=BOLD),
    )
    for btn in btnList:
        btn.config(state="disabled")
    canvas.update_idletasks()


def unblockBtn():
    # global btnList
    status.config(
        text="Sorting Complete!", foreground="#008000", font=Font(size=11, weight=BOLD)
    )
    for btn in btnList:
        btn.config(state="active")
    canvas.update_idletasks()


def clearCanvas():
    canvas.delete("all")


def shufflePipes():
    # global Global.y1CoorList, Global.sortdone
    status.config(
        text="Press a button to begin sorting", foreground="#000000", font=Font(size=9)
    )
    Global.y1CoorList = random.sample(
        range(0, y1Range, int(y1Range / no_of_pipes)), no_of_pipes
    )
    drawPipes()
    Global.sortdone = False
    print(Global.y1CoorList)


def drawPipes():
    # global Global.y1CoorList
    clearCanvas()
    x1 = -pipeWidth + gap * 2
    for i in range(no_of_pipes):
        x1 = x1 + pipeWidth + gap
        y1 = screenHeight - 10 - Global.y1CoorList[i]
        x2 = x1 + pipeWidth
        y2 = canvasHeight - 2
        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=pipeColors[int(Global.y1CoorList[i] / 4)].hex,
            outline="",
        )
    canvas.update()


def delay(sortSpeed):
    if Global.closeWindow:
        sys.exit()
    drawPipes()
    time.sleep(sortSpeed)


# algorithms below
def bubbleSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    num = n - 1
    swap = True
    while swap:
        swap = False
        for i in range(num):
            if Global.y1CoorList[i] > Global.y1CoorList[i + 1]:
                Global.y1CoorList[i], Global.y1CoorList[i + 1] = (
                    Global.y1CoorList[i + 1],
                    Global.y1CoorList[i],
                )
                swap = True
        delay(0.05)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def selectionSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if Global.y1CoorList[min_idx] > Global.y1CoorList[j]:
                min_idx = j
        Global.y1CoorList[i], Global.y1CoorList[min_idx] = (
            Global.y1CoorList[min_idx],
            Global.y1CoorList[i],
        )
        delay(0.05)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def insertionSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    for i in range(1, n):
        key = Global.y1CoorList[i]
        j = i - 1
        while j >= 0 and key < Global.y1CoorList[j]:
            Global.y1CoorList[j + 1] = Global.y1CoorList[j]
            j -= 1
        Global.y1CoorList[j + 1] = key
        delay(0.03)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def shellSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    incr = n // 2
    while incr > 0:
        for i in range(incr, n):
            temp = Global.y1CoorList[i]
            j = i
            while j >= incr and Global.y1CoorList[j - incr] > temp:
                Global.y1CoorList[j] = Global.y1CoorList[j - incr]
                j -= incr
            Global.y1CoorList[j] = temp
            if i % 3 == 0:
                delay(0)
        incr //= 2
    delay(0)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def counting(place):
    # global Global.y1CoorList
    Global.y1CoorListput = [0] * n
    count = [0] * 10
    for i in range(n):
        index = Global.y1CoorList[i] // place
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = Global.y1CoorList[i] // place
        Global.y1CoorListput[count[index % 10] - 1] = Global.y1CoorList[i]
        count[index % 10] -= 1
        i -= 1
    for i in range(n):
        Global.y1CoorList[i] = Global.y1CoorListput[i]
        delay(0)


def radixSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    max_element = max(Global.y1CoorList)
    place = 1
    while max_element // place > 0:
        counting(place)
        place *= 10
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def partition(low, high):
    # global Global.y1CoorList
    i = low - 1
    pivot = Global.y1CoorList[high]

    for j in range(low, high):
        if Global.y1CoorList[j] <= pivot:
            i = i + 1
            Global.y1CoorList[i], Global.y1CoorList[j] = (
                Global.y1CoorList[j],
                Global.y1CoorList[i],
            )
            delay(0)
    Global.y1CoorList[i + 1], Global.y1CoorList[high] = (
        Global.y1CoorList[high],
        Global.y1CoorList[i + 1],
    )
    return i + 1


def quickSort(low, high):
    # global Global.y1CoorList
    if low < high:
        pi = partition(low, high)
        quickSort(low, pi - 1)
        quickSort(pi + 1, high)


def callQuickSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    quickSort(0, n - 1)
    Global.sortdone = True
    unblockBtn()
    delay(0)
    print(Global.y1CoorList)


def mergeR(l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * (n1)
    R = [0] * (n2)
    for i in range(n1):
        L[i] = Global.y1CoorList[l + i]
    for j in range(n2):
        R[j] = Global.y1CoorList[m + 1 + j]
    i = 0  # Initial index of first subGlobal.y1CoorListay
    j = 0  # Initial index of second subGlobal.y1CoorListay
    k = l  # Initial index of merged subGlobal.y1CoorListay
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            Global.y1CoorList[k] = L[i]
            i += 1
        else:
            Global.y1CoorList[k] = R[j]
            j += 1
        k += 1
        delay(0)
    while i < n1:
        Global.y1CoorList[k] = L[i]
        i += 1
        k += 1
        delay(0)
    while j < n2:
        Global.y1CoorList[k] = R[j]
        j += 1
        k += 1
        delay(0)


def mergeSortR(l, r):
    if l < r:
        m = (l + (r - 1)) // 2
        mergeSortR(l, m)
        mergeSortR(m + 1, r)
        mergeR(l, m, r)


def callMergeSortR():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    mergeSortR(0, n - 1)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def cocktailSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if Global.y1CoorList[i] > Global.y1CoorList[i + 1]:
                Global.y1CoorList[i], Global.y1CoorList[i + 1] = (
                    Global.y1CoorList[i + 1],
                    Global.y1CoorList[i],
                )
                swapped = True
        delay(0.05)
        if not swapped:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if Global.y1CoorList[i] > Global.y1CoorList[i + 1]:
                Global.y1CoorList[i], Global.y1CoorList[i + 1] = (
                    Global.y1CoorList[i + 1],
                    Global.y1CoorList[i],
                )
                swapped = True
        delay(0.05)
        start += 1
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


RUN = 32


def insertionSortTim(left, right):
    # global Global.y1CoorList
    for i in range(left + 1, right + 1):
        temp = Global.y1CoorList[i]
        j = i - 1
        while Global.y1CoorList[j] > temp and j >= left:
            Global.y1CoorList[j + 1] = Global.y1CoorList[j]
            j -= 1
        Global.y1CoorList[j + 1] = temp
        delay(0)


def timSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    for i in range(0, n, RUN):
        insertionSortTim(i, min((i + 31), (n - 1)))
    size = RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = left + size - 1
            right = min((left + 2 * size - 1), (n - 1))
            mergeR(left, mid, right)
        size = 2 * size
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def heapify(n, i):
    # global Global.y1CoorList

    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2
    if l < n and Global.y1CoorList[i] < Global.y1CoorList[l]:
        largest = l
    if r < n and Global.y1CoorList[largest] < Global.y1CoorList[r]:
        largest = r
    if largest != i:
        Global.y1CoorList[i], Global.y1CoorList[largest] = (
            Global.y1CoorList[largest],
            Global.y1CoorList[i],
        )
        delay(0)
        heapify(n, largest)


def heapSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    for i in range(n, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        Global.y1CoorList[i], Global.y1CoorList[0] = (
            Global.y1CoorList[0],
            Global.y1CoorList[i],
        )
        heapify(i, 0)
    delay(0)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def countingSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    max_val = max(Global.y1CoorList)
    m = max_val + 1
    count = [0] * m
    for a in Global.y1CoorList:
        count[a] += 1

    i = 0
    for a in range(m):
        for _ in range(count[a]):
            Global.y1CoorList[i] = a
            i += 1
            delay(0.05)

    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def getNextGap(gap):
    gap = (gap * 10) / 13
    gap = int(gap)
    if gap < 1:
        return 1
    return gap


def combSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    gap = n
    swapped = True

    while gap != 1 or swapped == 1:
        gap = getNextGap(gap)
        swapped = False
        for i in range(n - gap):
            if Global.y1CoorList[i] > Global.y1CoorList[i + gap]:
                Global.y1CoorList[i], Global.y1CoorList[i + gap] = (
                    Global.y1CoorList[i + gap],
                    Global.y1CoorList[i],
                )
                swapped = True
                delay(0)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def pancakeSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    cur = n
    while cur > 1:
        mi = Global.y1CoorList.index(max(Global.y1CoorList[0:cur]))
        Global.y1CoorList = (
            Global.y1CoorList[mi::-1]
            + Global.y1CoorList[mi + 1 : len(Global.y1CoorList)]
        )
        Global.y1CoorList = (
            Global.y1CoorList[cur - 1 :: -1]
            + Global.y1CoorList[cur : len(Global.y1CoorList)]
        )
        cur -= 1
        delay(0.05)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def gnomeSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    for pos in range(1, len(Global.y1CoorList)):
        while pos != 0 and Global.y1CoorList[pos] < Global.y1CoorList[pos - 1]:
            Global.y1CoorList[pos], Global.y1CoorList[pos - 1] = (
                Global.y1CoorList[pos - 1],
                Global.y1CoorList[pos],
            )
            pos = pos - 1
        delay(0.01)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def oddEvenSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    isSorted = 0
    while isSorted == 0:
        isSorted = 1
        for i in range(1, n - 1, 2):
            if Global.y1CoorList[i] > Global.y1CoorList[i + 1]:
                Global.y1CoorList[i], Global.y1CoorList[i + 1] = (
                    Global.y1CoorList[i + 1],
                    Global.y1CoorList[i],
                )
                isSorted = 0
        for i in range(0, n - 1, 2):
            if Global.y1CoorList[i] > Global.y1CoorList[i + 1]:
                Global.y1CoorList[i], Global.y1CoorList[i + 1] = (
                    Global.y1CoorList[i + 1],
                    Global.y1CoorList[i],
                )
                isSorted = 0
        delay(0.05)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def stoogeSort(l, h, show):
    # global Global.y1CoorList
    if l >= h:
        return
    if Global.y1CoorList[l] > Global.y1CoorList[h]:
        Global.y1CoorList[h], Global.y1CoorList[l] = (
            Global.y1CoorList[l],
            Global.y1CoorList[h],
        )
        if show:
            delay(0)

    if h - l > 1:
        t = (int)((h - l + 2) / 3)
        stoogeSort(l, (h - t), 1)
        stoogeSort(l + t, (h), 0)
        stoogeSort(l, (h - t), 0)


def callStoogeSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    stoogeSort(0, n - 1, 0)
    cycleSort()
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def introsort_helper(start, end, maxdepth):
    # global Global.y1CoorList
    if end - start <= 1:
        return
    if maxdepth == 0:
        heapsort2(start, end)
    else:
        p = partition2(start, end)
        introsort_helper(start, p + 1, maxdepth - 1)
        introsort_helper(p + 1, end, maxdepth - 1)


def partition2(start, end):
    # global Global.y1CoorList
    pivot = Global.y1CoorList[start]
    i = start - 1
    j = end
    while True:
        i = i + 1
        while Global.y1CoorList[i] < pivot:
            i = i + 1
        j = j - 1
        while Global.y1CoorList[j] > pivot:
            j = j - 1
        if i >= j:
            return j
        swap(i, j)
        delay(0.01)


def swap(i, j):
    # global Global.y1CoorList
    Global.y1CoorList[i], Global.y1CoorList[j] = (
        Global.y1CoorList[j],
        Global.y1CoorList[i],
    )


def heapsort2(start, end):
    # global Global.y1CoorList
    build_max_heap(start, end)
    for i in range(end - 1, start, -1):
        swap(start, i)
        max_heapify(index=0, start=start, end=i)


def build_max_heap(start, end):
    # global Global.y1CoorList

    def parent(i):
        return (i - 1) // 2

    length = end - start
    index = parent(length - 1)
    while index >= 0:
        max_heapify(index, start, end)
        index = index - 1


def max_heapify(index, start, end):
    # global Global.y1CoorList

    def left(i):
        return 2 * i + 1

    def right(i):
        return 2 * i + 2

    size = end - start
    l = left(index)
    r = right(index)
    if l < size and Global.y1CoorList[start + l] > Global.y1CoorList[start + index]:
        largest = l
    else:
        largest = index
    if r < size and Global.y1CoorList[start + r] > Global.y1CoorList[start + largest]:
        largest = r
    if largest != index:
        swap(start + largest, start + index)
        max_heapify(largest, start, end)


def introSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    maxdepth = (len(Global.y1CoorList).bit_length() - 1) * 2
    introsort_helper(0, n, maxdepth)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def cycleSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    writes = 0
    for cycleStart in range(len(Global.y1CoorList) - 1):
        item = Global.y1CoorList[cycleStart]
        pos = cycleStart
        for i in range(cycleStart + 1, len(Global.y1CoorList)):
            if Global.y1CoorList[i] < item:
                pos += 1
        if pos == cycleStart:
            continue
        while item == Global.y1CoorList[pos]:
            pos += 1
        Global.y1CoorList[pos], item = item, Global.y1CoorList[pos]
        writes += 1
        while pos != cycleStart:
            pos = cycleStart
            for i in range(cycleStart + 1, len(Global.y1CoorList)):
                if Global.y1CoorList[i] < item:
                    pos += 1
            while item == Global.y1CoorList[pos]:
                pos += 1

            Global.y1CoorList[pos], item = item, Global.y1CoorList[pos]
            writes += 1
            delay(0)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def beadSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    maximum = max(Global.y1CoorList)
    beads = [[0] * maximum for _ in range(n)]

    for i in range(n):
        for j in range(Global.y1CoorList[i]):
            beads[i][j] = 1
    for j in range(maximum):
        drop_beads_by_column = 0
        for i in range(n):
            drop_beads_by_column += beads[i][j]
            beads[i][j] = 0
        for i in range(n - 1, n - drop_beads_by_column - 1, -1):
            beads[i][j] = 1
        for i in range(n):
            num_beads_in_row = beads[i].count(1)
            Global.y1CoorList[i] = num_beads_in_row
        delay(0)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def mergeSortI():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    unit = 1
    while unit <= n:
        h = 0
        for h in range(0, n, unit * 2):
            l, r = h, min(n, h + 2 * unit)
            mid = h + unit
            p, q = l, mid
            while p < mid and q < r:
                if Global.y1CoorList[p] <= Global.y1CoorList[q]:
                    p += 1
                else:
                    tmp = Global.y1CoorList[q]
                    Global.y1CoorList[p + 1 : q + 1] = Global.y1CoorList[p:q]
                    Global.y1CoorList[p] = tmp
                    p, mid, q = p + 1, mid + 1, q + 1
                    delay(0.01)
        unit *= 2
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def dual_pivot_sort(start, top):
    # global Global.y1CoorList
    if top <= start:
        return
    p = start
    q = top
    k = p + 1
    h = k
    l = q - 1
    if Global.y1CoorList[p] > Global.y1CoorList[q]:
        Global.y1CoorList[p], Global.y1CoorList[q] = (
            Global.y1CoorList[q],
            Global.y1CoorList[p],
        )
    while k <= l:
        if Global.y1CoorList[k] < Global.y1CoorList[p]:
            Global.y1CoorList[h], Global.y1CoorList[k] = (
                Global.y1CoorList[k],
                Global.y1CoorList[h],
            )
            h += 1
            k += 1
            delay(0.0)
        elif Global.y1CoorList[k] > Global.y1CoorList[q]:
            Global.y1CoorList[k], Global.y1CoorList[l] = (
                Global.y1CoorList[l],
                Global.y1CoorList[k],
            )
            l -= 1
            delay(0.0)
        else:
            k += 1
    h -= 1
    l += 1
    Global.y1CoorList[p], Global.y1CoorList[h] = (
        Global.y1CoorList[h],
        Global.y1CoorList[p],
    )
    # delay(0)
    Global.y1CoorList[q], Global.y1CoorList[l] = (
        Global.y1CoorList[l],
        Global.y1CoorList[q],
    )
    # delay(0)
    dual_pivot_sort(start, h - 1)
    dual_pivot_sort(h + 1, l - 1)
    dual_pivot_sort(l + 1, top)


def callDPQuickSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    dual_pivot_sort(0, n - 1)
    delay(0)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


def compAndSwap(i, j, dire):
    # global Global.y1CoorList
    if (dire == 1 and Global.y1CoorList[i] > Global.y1CoorList[j]) or (
        dire == 0 and Global.y1CoorList[i] < Global.y1CoorList[j]
    ):
        Global.y1CoorList[i], Global.y1CoorList[j] = (
            Global.y1CoorList[j],
            Global.y1CoorList[i],
        )
        delay(0)


def bitonicMerge(low, cnt, dire):
    # global Global.y1CoorList
    if cnt > 1:
        k = int(cnt / 2)
        for i in range(low, low + k):
            compAndSwap(i, i + k, dire)
        bitonicMerge(low, k, dire)
        bitonicMerge(low + k, k, dire)


def bitonicSort(low, cnt, dire):
    if cnt > 1:
        k = int(cnt / 2)
        bitonicSort(low, k, 1)
        bitonicSort(low + k, k, 0)
        bitonicMerge(low, cnt, dire)


def callBitonicSort():
    # global Global.y1CoorList, Global.sortdone
    if not check_sortdone():
        return
    blockBtn()
    up = 1
    bitonicSort(0, len(Global.y1CoorList), up)
    Global.sortdone = True
    unblockBtn()
    print(Global.y1CoorList)


# UI related code below
screen.update()
b1 = Button(
    screen,
    text="Shuffle",
    image=pixelVirtual,
    width=screenWidth - canvasWidth - 28,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=shufflePipes,
)
b1.place(x=canvasWidth + 10, y=5 + 30 * 0)
b2 = Button(
    screen,
    text="Bubble Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=bubbleSort,
)
b2.place(x=canvasWidth + 10, y=5 + 30 * 2)
b3 = Button(
    screen,
    text="Selection Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=selectionSort,
)
b3.place(x=canvasWidth + 10, y=5 + 30 * 3)
b4 = Button(
    screen,
    text="Insertion Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=insertionSort,
)
b4.place(x=canvasWidth + 10, y=5 + 30 * 4)
b5 = Button(
    screen,
    text="Shell Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=shellSort,
)
b5.place(x=canvasWidth + 10, y=5 + 30 * 5)
b6 = Button(
    screen,
    text="Radix Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=radixSort,
)
b6.place(x=canvasWidth + 10, y=5 + 30 * 6)
b7 = Button(
    screen,
    text="Quick Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=callQuickSort,
)
b7.place(x=canvasWidth + 10, y=5 + 30 * 7)
b8 = Button(
    screen,
    text="Merge Sort (R)",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=callMergeSortR,
)
b8.place(x=canvasWidth + 10, y=5 + 30 * 8)
b9 = Button(
    screen,
    text="Cocktail Shaker Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=cocktailSort,
)
b9.place(x=canvasWidth + 10, y=5 + 30 * 9)
b10 = Button(
    screen,
    text="Tim Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=timSort,
)
b10.place(x=canvasWidth + 10, y=5 + 30 * 10)
b11 = Button(
    screen,
    text="Heap Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=heapSort,
)
b11.place(x=canvasWidth + 10, y=5 + 30 * 11)
b12 = Button(
    screen,
    text="Counting Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=countingSort,
)
b12.place(x=canvasWidth + 10, y=5 + 30 * 12)
b13 = Button(
    screen,
    text="Comb Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=combSort,
)
b13.place(x=canvasWidth + 10, y=5 + 30 * 13)
b14 = Button(
    screen,
    text="Pancake Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=pancakeSort,
)
b14.place(x=canvasWidth + 10, y=5 + 30 * 14)
b15 = Button(
    screen,
    text="Gnome Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=gnomeSort,
)
b15.place(x=canvasWidth + 10, y=5 + 30 * 15)
b16 = Button(
    screen,
    text="Odd Even Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=oddEvenSort,
)
b16.place(x=canvasWidth + 10 * 15, y=5 + 30 * 2)
b17 = Button(
    screen,
    text="Stooge Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=callStoogeSort,
)
b17.place(x=canvasWidth + 10 * 15, y=5 + 30 * 3)
b18 = Button(
    screen,
    text="Intro Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=introSort,
)
b18.place(x=canvasWidth + 10 * 15, y=5 + 30 * 4)
b19 = Button(
    screen,
    text="Cycle Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=cycleSort,
)
b19.place(x=canvasWidth + 10 * 15, y=5 + 30 * 5)
b20 = Button(
    screen,
    text="Bead Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=beadSort,
)
b20.place(x=canvasWidth + 10 * 15, y=5 + 30 * 6)
b21 = Button(
    screen,
    text="Merge Sort (I)",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=mergeSortI,
)
b21.place(x=canvasWidth + 10 * 15, y=5 + 30 * 7)

b22 = Button(
    screen,
    text="Dual Pivot Quick Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=callDPQuickSort,
)
b22.place(x=canvasWidth + 10 * 15, y=5 + 30 * 8)
b23 = Button(
    screen,
    text="Bitonic Sort",
    image=pixelVirtual,
    width=110,
    compound="c",
    relief="groove",
    activebackground="white",
    bg="white",
    command=callBitonicSort,
)
b23.place(x=canvasWidth + 10 * 15, y=5 + 30 * 9)


btnList = [
    b1,
    b2,
    b3,
    b4,
    b5,
    b6,
    b7,
    b8,
    b9,
    b10,
    b11,
    b12,
    b13,
    b14,
    b15,
    b16,
    b17,
    b18,
    b19,
    b20,
    b21,
    b22,
    b23,
]

toplabel = Label(
    screen,
    text="Available Sorts",
    image=pixelVirtual,
    width=screenWidth - canvasWidth - 28,
    height=20,
    compound="c",
    bg="white",
    font=Font(family="calibri", size=12, weight=BOLD),
)
toplabel.place(x=canvasWidth + 10, y=5 + 30 * 1)
status = Label(
    screen,
    text="Press a button to begin sorting",
    image=pixelVirtual,
    width=screenWidth - canvasWidth - 28,
    height=20,
    compound="c",
    background="white",
    relief="groove",
    font=Font(size=9),
)
status.place(x=canvasWidth + 10, y=5 + 30 * 16)


drawPipes()


def _delete_window():
    # global closeWindow
    print("delete_window")
    Global.closeWindow = True
    # clearCanvas()
    # canvas.destroy()
    screen.quit()


screen.protocol("WM_DELETE_WINDOW", _delete_window)
screen.mainloop()
