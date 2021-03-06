import helper_functions as hf
import tlb_pagetable as tp

physicalMemory = {}
tlb = []
pageTable = []
pageFaultCounter = 0
tlbHitCounter = 0
addressReadCounter = 0


if __name__ == '__main__':
    outputFile = open('mappings.txt', 'w')

    with open('virtualAddress.txt', 'r') as addressFile:
        for line in addressFile:
            tlbHit = 0
            pageTableTrue = 0

            logicalAddress = int(line)
            offset = logicalAddress & 255
            pageOriginal = logicalAddress & 65280
            pageNumber = pageOriginal >> 8
            # print("Logical address is: " + str(logicalAddress) +
            #       "\nPageNumber is: " + str(pageNumber) + "\nOffset: " + str(offset))
            addressReadCounter += 1

            tlbHit = tp.checkTLB(pageNumber, physicalMemory, offset,
                                 logicalAddress, tlb, addressReadCounter, outputFile)

            if tlbHit == 1:
                tlbHitCounter += 1

            if tlbHit != 1:
                pageTableTrue = tp.checkPageTable(
                    pageNumber, logicalAddress, offset, addressReadCounter, pageTable, physicalMemory, outputFile)

            if pageTableTrue != 1 and tlbHit != 1:
                # print("This is a page fault!")
                hf.pageFaultHandler(
                    pageNumber, tlb, pageTable, physicalMemory)
                pageFaultCounter += 1
                tp.checkTLB(pageNumber, physicalMemory, offset,
                            logicalAddress, tlb, addressReadCounter, outputFile)

    pageFaultRate = pageFaultCounter / addressReadCounter
    tlbHitRate = tlbHitCounter / addressReadCounter
    outStr = 'Number of translated address: ' + str(addressReadCounter) + '\n' + 'Number of page fault: ' + str(
        pageFaultCounter) + '\n' + 'Page fault rate: ' + str(pageFaultRate) + '\n' + 'Number of TLB hits: ' + str(
        tlbHitCounter) + '\n' + 'TLB hit rate: ' + str(tlbHitRate) + '\n'
    # print(outStr)
    if outputFile.write(outStr):
        print("Successful")
    outputFile.close()
    addressFile.close()
