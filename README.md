# ReplyChallenge
Solution to [Reply Challenge Optimization Problem on March 12 2020](https://challenges.reply.com/tamtamy/challenges/category/coding) using Genetic Algorithm 

## Brief Description:
  - let we number all available cells for Developer and Managers on map (like [1, 5, 7, 8] for devs, [4, 3, 1] for mans)
  - let represent one **seating** (like dev1 on 1, dev5 sits on 5 cell, man1 seats on cell 17 etc.) as **Individual** 
  - then we can create **Population** from it (take 1000 random seatings for first population), apply **crossovers** (like create  new seating for population: take dev1 seating at cell 5, dev2 seating on cell 6 from one  one seating, but man1 and dev3 ceating at cell 7/8 (for example) from other population/and **mutations** (randomly change seating dev1 to non seating dev2 etc)
  - choose N **best** seating and then **evolve** population again, do it until for example 1000 **epochs** were processed

Sorry for VERY DISGUSTING code, I wrote it all by myself in less than 4 hours (but this was contest for teams).  
I had no time to submit it, but at least let this code remind me
about me having a good time coding this sh*t 
