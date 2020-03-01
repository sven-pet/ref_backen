---
toc:
  depth_from: 1
  depth_to: 3
  ordered: false
---

[TOC]

# Project Referendum

*This is the first documentation of the Project Referendum. The idea idea behind the project is to eneable secure persenoal login with the possibility to make your boice heard. This will also supply correct and authentic*


## Architecture

### Users

##### Participant
The Participant is a verified user with the right to vote in the selected referendum. For example this can be a citizen of a country that the referendum will refelct.

##### Referendum administrator
This is the Administration of the referendum.

##### Referendum viewer
The view of the referendum is presnted here.

### Parts
##### Participant device
The device that the participant will use to log into the referendum and answer the questions

##### Referendum handler
A data server that the Praticipant connects to to answer the referendum. This server will:
- Ensure that only a verified participant of a specific population can vote
- Ensure that a verified person only can place one vote.
- Conduct the verification of the user
- Anonymize the participant so it is not possible to fetch information about who the participant is. This apart from genereal information that can be set when creating the referendum. But in the end it should not be possible to se who voted what.

##### Data provider
The collection of data that shouold be provided to the referendum. This can either be a totaly seperate system that uses the rest api presented by the referendum handler.

##### SCA Provider
A provider of SCA login. This is used to verify that the participant is a real person.

##### KYC Provider
A provider of KYC of participant. This is used to fetch extra information about participant. For example age, registered adress and similar.

### Sequence diagrams

##### Casting vote
```puml
actor Participant as p
control "Referendum Handler" as rh
database "Referendum Database" as rdata
collections "Referendum Data" as rd
control "SCA Provider" as SCA
control "KYC Provider" as KYC


p -> rh: Authentication Request

rh -> rdata: Get referendum id
rdata -> rh: Referendum id
rh -> rd: Request to fetch data of referendum
rd -> rh: Return data of referendum
rh -> rdata: Check status of participant
rdata -> rh: Status of participation returned
rd ->p: Return data of referendum + status of participation

p -> rh: Request to vote
rh -> rdata: Check status of participant
group user has not voted yet
rdata -> rh: Participant has not voted
  rh -> SCA: handle SCA for user
  SCA -> rh: User verified and alias returned
  rh -> KYC: fetch community where user lives
  KYC -> rh: community
  rh -> rdata: check if user is allowed to vote
  group user allowed to vote
    rdata -> rh: allowed to vote
    rh -> p: ask for vote
    p -> rh: cast vote
    rh -> rdata: cast vote
    rdata -> rh: voted cast
    rh -> p: voted cast
  end
  group user not allowed to vote
    rdata -> rh: user not allowed to vote
    rh -> p: vote declined with reason
  end
end
     







```





