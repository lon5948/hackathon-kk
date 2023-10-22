document.getElementById("urlForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const url = document.getElementById("url").value;

  if (url.trim() !== "") {
    localStorage.setItem("url", url);
  } else {
    localStorage.setItem(
      "url",
      "https://showroom.one-stage.kkstream.io?token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3N2RhODVjLTllZjgtNTVjYS05M2FkLTAyYTMyZjkwZjg2MyIsInR5cCI6IkpXVCJ9.eyJyZXNvdXJjZV9pZCI6IjRkNDA4NjAwLTZmZGItNGY4OS1hNWFhLTk0NzFkZGViZDJjZSIsInJlc291cmNlX3R5cGUiOiJSRVNPVVJDRV9UWVBFX0xJVkVfRVZFTlQifQ.LzxwhXuqVvAm7I6TDRmorMtVZBZkwkLHv7I3vVPKTOlgwJSEZVBpPll9Wun0e2gIpU8Wk70wNUo9nQh_B5pAmGsNhfJyul0-5Fc2uk0SGAiGBag1wPDtjXrXrSLL-OHqMp-xrh2oDouJXV6SWCuadp33BDdnFIpXeqd3kIeU9xCyJRBahqfFDhr5SofI740aNoHdD8ueYoFWpp1M4UoZxN6l8S8eTUbnSH5Dioy8uOZc5dZsm2LPdglHOWbtDEI5q8CML1LUQzzmtgT4pmLfHtscopqsXy_2GTjjusS5T92SlbcYwYB9kqc9vdFYUg0kJLJPyS9Z_my5Iz_7vqP4bXrO_zkk4vybH3NrBFWhiGcr-ZahF1D9qYv9js6Z2SaGmA-sEFZuKZchART_qvrBpfPElZJN6D8Z_-n7HyH17Ky-Z7mQhuIm7GaoY2S3W-Ai2JWDxsas4T4Uer4uWxUvGjTxosTJMvj5sKx7caZjcHrDUsZLv5d_Yx9-hSiuhsFMoPH32vXe2Im1j67_P7bWqiLPU-ECkquHuPzHT0fY1Zw6Ow-YmfDMCvvMi9aajgP7EG0m5tq6pJFxEn9-YeZIcfJtTRsdVMAZQ7WyIWsPSfofZW3v4IcASvOVVL3BzTHBMxWpFs4hRb3aDjARAKYoBmj1f5L6dILAEceW6HR55fw"
    );
  }
  window.location.href = "chatroom.html";
});
