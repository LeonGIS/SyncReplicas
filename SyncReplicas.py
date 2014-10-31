# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# SyncReplicas.py
# Created on: 2014-10-20 16:19:04.00000

# Description: 
# Reads in command line arguements for synchronizing replicas for ArcGIS

# Command Line Example: 
# SyncReplicas.py -p "Database Connections\\geoParcels.sde"  -c "\\arcgisweb\\arcgisserver\\serverdata\\public\\agspub.gdb" -i "C:\development\Python\SyncReplicas\agspub.txt" -l "C:\development\Python\SyncReplicas\Sync.log"
#
# Command Line Arguments
# -p: Parent geodatabase connection
# -c: Child geodatabase connection
# -i: CSV file of replicas to sync between parent and child
# -l: Log file

# Input file Example
# ParentReplica,ChildReplica,Direction,ConflictRes,ConflictDetect
# DBO.GeoparcelsToAGSPub,GeoparcelsToAGSPub,FROM_GEODATABASE1_TO_2,MANUAL,BY_ATTRIBUTE

# Input file format
# Required field header: ParentReplica,ChildReplica,,Direction,ConflictRes,ConflictDetect
# Parent Replica: Name of valid replica
# Child Replica: Name of valid replica
# Direcion: Valid options (BOTH_DIRECTIONS, FROM_GEODATABASE2_TO_1, FROM_GEODATABASE1_TO_2)  See ArcGIS help for Synchronzize changes tool
# ConflictRes: Conflict resolution options (MANUAL, IN_FAVOR_OF_GDB1, IN_FAVOR_OF_GDB2)   See ArcGIS help for Synchronzize changes tool
# ConflictDetect: How conflicts are defined options (BY_OBJECT, BY_ATTRIBUTE) See ArcGIS help for Synchronzize changes tool
#---------------------------------------------------------------------------

# Set the necessary product code
import arceditor

# Import arcpy module
import arcpy
import logging
import sys, getopt
import csv

def main(argv):
    print 'start'
    
    try:
      opts, args = getopt.getopt(argv,"p:c:i:l:",["parentconn=","childconn=","inputlist=","logfile="])
    except getopt.GetoptError:
      print 'test.py -p <parentconnection> -a <parenttype> -c <childconnection> -h <childtype> -i <inputlist> -l <logfile>'
      sys.exit(2)

    print 'parse options'

    for o, a in opts:
        if o in ("-p", "--parentconn"):
            ParentConn = a
        elif o in ("-c", "--childconn"):
            ChildConn = a
        elif o in ("-i", "--inputlist"):
            InputList = a
        elif o in ("-l", "--logfile"):
            LOG_FILENAME = a
        else:
            assert False, "unhandled option"

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=  LOG_FILENAME,
                        filemode='a')

    # Local variables:
    try:
        todo = csv.DictReader(open(InputList, 'r'),  delimiter=',')
    except:
        logging.info('Failed to read input list!')
        sys.exit(2)

    for row in todo:
        print row
        ParentReplica = row.get('ParentReplica')
        ChildReplica = row.get('ChildReplica')
        Direction = row.get('Direction')
        ConflictRes = row.get('ConflictRes')
        ConflictDetect =  row.get('ConflictDetect')
    
        # Verify parent replica
        blnFoundParent = False
        for parentrep in arcpy.da.ListReplicas(ParentConn):
            if parentrep.name == ParentReplica: 
                blnFoundParent = True
                break
        if not blnFoundParent:
            logging.info(ParentReplica + " not found on parent")  
          
        # Verify child replica
        blnFoundChild = False
        for childrep in arcpy.da.ListReplicas(ChildConn):
            if childrep.name == ChildReplica: 
                blnFoundChild = True
                break
        if not blnFoundChild:
            logging.info(ChildReplica + " not found on child")  
           
        if blnFoundChild & blnFoundParent:
            # Process: Synchronize Changes
            try:
                arcpy.SynchronizeChanges_management(ParentConn, ParentReplica, ChildConn, Direction, ConflictRes, ConflictDetect, "DO_NOT_RECONCILE")
                logging.info('Sync ' + ParentReplica)  
            except:
                logging.info('Sync ' + ParentReplica + " - " + arcpy.GetMessages(2))

    logging.info('Complete Sync *********************************')

if __name__ == "__main__":
   main(sys.argv[1:])