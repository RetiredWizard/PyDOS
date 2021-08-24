10 print tab (33),"CHOMP"
20 print tab (15),"CREATIVE COMPUTING MORRISTOWN, NEW JERSEY"
30 print
31 print
32 print
40 dim a(11,11)
100 rem *** THE GAME OF CHOMP *** COPYRIGHT PCC 1973 ***
110 print
120 print "THIS IS THE GAME OF CHOMP (SCIENTIFIC AMERICAN, JAN 1973)"
130 print "WANT THE RULES (1=YES, 0=NO!)";
140 input r
150 if r = 0 then 340
160 f = 1
170 r = 5
180 c = 7
190 print "CHOMP IS FOR ONE OR MORE PLAYERS (HUMANS ONLY)."
200 print
210 print "HERE'S HOW A BOARD LOOKS (THIS ONE IS 5 BY 7):"
220 gosub 540
230 print
240 print "THE BOARD IS A BIG COOKIE - R ROWS HIGH AND C COLUMNS"
250 print "WIDE. YOU INPUT R AND C AT THE START. IN THE UPPER LEFT"
260 print "CORNER OF THE COOKIE IS A POSION SQUARE (P). THE ONE WHO"
270 print "CHOMPS THE POSION SQUARE LOSES. TO TAKE A CHOMP TYPE THE"
280 print "ROW AND COLUMN OF ONE OF THE SQUARES ON THE COOKIE."
290 print "ALL OF THE SQUARES BELOW AND TO THE RIGHT OF THAT SQUARE"
300 print "(INCLUDING THAT SQUARE, TOO) DISAPPEAR -- CHOMP!!"
310 print "NO FAIR CHOMPING SQUARES THAT HAVE ALREADY BEEN CHOMPED,"
320 print "OR THAT ARE OUTSIDE THE ORIGINAL DIMENSION OF THE COOKIE."
330 print
340 print "HERE WE GO..."
350 rem
360 f = 0
370 for i = 1 to 10
372 for j = 1 to 10
375 a(i,j) = 0
377 next j
379 next i
380 print
390 print "HOW MANY PLAYERS? ";
400 input p
410 i1 = 0
420 print "HOW MANY ROWS? ";
430 input r
440 if r <= 9 then 470
450 print "TOO MANY ROWS (9 IS MAXIMUM). NOW, ";
460 goto 420
470 print "HOW MANY COLUMNS? ";
480 input c
490 if c <= 9 then 530
500 print "TOO MANY COLUMNS (9 IS MAXIMUM). NOW, ";
510 goto 470
530 print
540 for i = 1 to r
550 for j = 1 to c
560 a(i,j) = 1
570 next j
580 next i
590 a(1,1) = -1
600 rem PRINT THE BOARD
610 print
620 print tab (7),"1 2 3 4 5 6 7 8 9"
630 for i = 1 to r
640 print i,tab (7);
650 for j = 1 to c
660 if a(i,j) = -1 then 700
670 if a(i,j) = 0 then 730
680 print "* ";
690 goto 710
700 print "P ";
710 next j
720 print
730 next i
740 print
750 if f = 0 then 770
760 return
770 rem GET CHOMPS FOR EACH PLAYER IN TURN
780 let i1 = i1+1
790 let p1 = i1-int(i1/p)*p
800 if p1 <> 0 then 820
810 p1 = p
820 print "PLAYER ",p1
830 print "COORDINATES OF CHOMP (ROW,COLUMN) ";
840 input r1,c1
850 if r1 < 1 then 920
860 if r1 > r then 920
870 if c1 < 1 then 920
880 if c1 > c then 920
890 if a(r1,c1) = 0 then 920
900 if a(r1,c1) = -1 then 1010
910 goto 940
920 print "NO FAIR. YOU'RE TRYING TO CHOMP ON AN EMPTY SQUARE!"
930 goto 820
940 for i = r1 to r
950 for j = c1 to c
960 a(i,j) = 0
970 next j
980 next i
990 goto 610
1000 rem END OF GAME DETECTED IN LINE 900
1010 print "YOU LOSE, PLAYER ",p1
1020 print
1030 print "AGAIN? (1=YES, 0=NO!) ";
1040 input r
1050 if r = 1 then 340
1060 end
