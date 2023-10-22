document.getElementById("urlForm").addEventListener("submit", function (event) {
event.preventDefault();

const url = document.getElementById("url").value;

if (url.trim() !== "") {
    sessionStorage.setItem("url", url);
    
} else {
    sessionStorage.setItem("url", "https://showroom.one-stage.kkstream.io?token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3N2RhODVjLTllZjgtNTVjYS05M2FkLTAyYTMyZjkwZjg2MyIsInR5cCI6IkpXVCJ9.eyJyZXNvdXJjZV9pZCI6IjZkOTc0MDFkLTAxZDYtNDY4Ny05NTRmLWE3NGZiN2EzNWJkMCIsInJlc291cmNlX3R5cGUiOiJSRVNPVVJDRV9UWVBFX0xJVkVfRVZFTlQifQ.H3NDCRViL9ieUC_KEsGM1bGo1KtWStPc_Irwze7NCcm6Rf5sK6UWU2TGQs2yO5yOGilfu3ksV5HvXvMsQFk_4VHjR467YE77QwSwrndwdX79vvB-ST0semKngkZqzWp9XcWrez9ACZSImtTWl2fyhmTkB-ykPLuq98Sk3tf79oZ9PmvTK08AOkYu-xssv559RoCvxlQN24Wx-um1HTzXwGqXYD_4hB07dIPdXSFX41yMZP3S61-Qdm4-7o_jZV6BzwBev-ztkYGAJZI3EUmwueqotHdMipB69w7uYeoLvghFGPClUqOu446bvCWSPpeB8hsInsgEp89JnX2P3HdguD0oj8Hd6F_TYS9n5yPuwbfyF09lPVYns6vCSokFS1gSMWVKa4AWIWYsHzU_1oJhAxfkmELRB-VA7dPa-0T6z9hy8_VBkA2w7C5ejXrySNuuh5-gfhKKzRL_mRs8vjIm4MJXghuolFrMGNdpZlSWq4htplHzP0cSX6mny2SCI8u8_4ICmMmPiJVaJ6syqLLr8vjJph-0leBIgYavWQXtUOeEaRgaod4wqN7gB2VrepBxu2zIA9aHcH_UDD2FBYMsKwUI3LbsImvuGcvGDXOpTJK3FWQpQ77fPvE9DshlVWuHojJidA5YsvH9Eyba8Dc-wJRpxFTvQHEfPgeBTFnWvm4");
}
window.location.href = "chatroom.html";
});