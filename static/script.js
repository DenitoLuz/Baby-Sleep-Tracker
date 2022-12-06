function showPass() {
    var x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

  function setTime(element){
  var today = new Date();
    var time = doubleDig(today.getHours()) + ":" + doubleDig(today.getMinutes());
    var date = today.getFullYear()+'-'+doubleDig((today.getMonth()+1))+'-'+doubleDig(today.getDate());
    document.getElementById(element).value = time;
    if (element == 'sleep')
    {
      document.getElementById('date').value = date;
    }

    console.log(time);
  }

  function doubleDig(num){

    if (parseInt(num)< 10)
    {
      num = '0'+num;
    }
    return num;
  }