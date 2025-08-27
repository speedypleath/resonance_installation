function bucket(x) {
    if (x < -0.33)       return "low";
    else if (x >  0.33)  return "high";
    else                 return "mid";
}


function list(v, a, d) {
  var key = "V" + bucket(v) + "_A" + bucket(a) + "_D" + bucket(d);
  outlet(0, key);
}