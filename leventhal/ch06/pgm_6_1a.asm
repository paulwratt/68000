DATA     EQU     $6000
PROGRAM  EQU     $4000

         ORG     DATA
START    DS.L    1               ADDRESS OF STRING
LENGTH   DS.W    1               NUMBER OF CHARACTERS IN STRING

CR       EQU     $0D             ASCII VALUE FOR CARRIAGE RETURN

         ORG     PROGRAM

PGM_6_1A MOVEA.L START,A0        POINTER TO START OF STRING
         MOVEQ   #0,D0           INITIALIZE LENGTH COUNTER

LOOP     CMPI.B  #CR,(A0)+       IS CURRENT CHAR A CARRIAGE RETURN?
         BEQ.S   DONE            IF YES THEN DONE

         ADDQ.W  #1,D0           ...ELSE INCREMENT LENGTH COUNTER
         BRA     LOOP            CONTINUE SCAN

DONE     MOVE.W  D0,LENGTH       SAVE STRING LENGTH

         RTS

         END     PGM_6_1A