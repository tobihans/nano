import "basecoat-css/all";
import Alpine from "alpinejs";
import ajax from "@imacrayon/alpine-ajax";

Alpine.plugin(ajax);

// window.Alpine = Alpine;

document.addEventListener("DOMContentLoaded", () => Alpine.start());
