
document.addEventListener("DOMContentLoaded", () => {
    console.log('hello')
    const toaster = document.querySelector(".toaster");
    const btn = document.getElementById("btn");
  
    console.log(toaster);
  
    btn.addEventListener("click", () => {
        console.log('click')

      const fadeToastOut = setTimeout(() => {
        toaster.classList.remove("show");
        console.log("removing", fadeToastOut);
      }, 4000);
  
      if (toaster.classList.contains("show")) {
        clearTimeout(fadeToastOut);
      }
      toaster.classList.add("show");
    });
  });
  