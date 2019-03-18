window.onload=function() {
    var cells = document.getElementById('table1').getElementsByTagName('td');
    for (var i=0, n=cells.length;i<n;i++) {
      cells[i].onclick=function() { alert(this.innerHTML) }
    }
  }