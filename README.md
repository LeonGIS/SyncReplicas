Name - SyncReplicas
Description - Reads in command line arguements for synchronizing replicas for Esri geodatabases

Command Line Example: 
SyncReplicas.py -p "Database Connections\\YourDb.sde"  -c "\\YourServer\\serverdata\\YourRemotePub.gdb" -i "C:\development\Python\SyncReplicas\agspub.txt" -l "C:\development\Python\SyncReplicas\Sync.log"

Command Line Arguments
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
