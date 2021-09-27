from voiceit2 import VoiceIt2
import pyaudio
import wave

#print(frames)
my_voiceit = VoiceIt2('key_56c24a5f4d4e41268ad35e3cc73eaca0','tok_132c2d00a38449179502fc4ed5a84f55')
print(my_voiceit)
#print(frames)
#print(len(frames))
user=my_voiceit.create_user()
print(user)
print('\n\n\n\n\n\n')
users=my_voiceit.get_all_users()
print(users)
userId_vip = 'usr_69297c47a3984f149741bdeee6ab78fe'
userId_krit='usr_15a9d48807a64cd282841957b36cc41c'
userId_ish='usr_053ea74d2faa4b3e91c623ac80216f85'
#print(user)
#userId='usr_69297c47a3984f149741bdeee6ab78fe'
# check_user_details=my_voiceit.check_user_exists(userId)
# print(check_user_details)
# voices=my_voiceit.create_voice_enrollment(userId, "no-STT", "never forget tomorrow is a new day", "ish (3).mpeg")

#voices=my_voiceit.get_all_voice_enrollments(userId)
# print(voices)
# ver=my_voiceit.voice_verification("usr_69297c47a3984f149741bdeee6ab78fe", "no-STT", "never forget tomorrow is a new day", "pa1.mp4")
# print(ver)


#group_created=my_voiceit.create_group("Welcome to Krishvi Xethon")
groups=my_voiceit.get_all_groups()
# print(groups)
groupId='grp_10a96522eb114182bafeb5c51bc40ab6'
# user1=my_voiceit.add_user_to_group(groupId, userId_ish)
# print(user1)
# user1=my_voiceit.add_user_to_group(groupId, userId_vip)
# print(user1)
# user1=my_voiceit.add_user_to_group(groupId, userId_krit)
# print(user1)
identified_as=my_voiceit.voice_identification(groupId, "no-STT", "never forget tomorrow is a new day","pa4.mp4")
print(identified_as)