import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";
import Notifications from "./notifications.jsx";
import img from "../../img/m101.jpg";
import "../../styles/sidebar.css";


const Sidebar = () => {
  const { store, actions } = useContext(Context);
  const [style, setStyle] = useState("discover");
  const [navbarHeight, setNavbarHeight] = useState(0);

  useEffect(() => {
    // Get the height of the navbar and set it to state
    const navbarElement = document.querySelector(".navbar");
    if (navbarElement) {
      setNavbarHeight(navbarElement.offsetHeight);
    }

    // Show the offcanvas by default
    const offcanvasElement = document.getElementById("offcanvasScrolling3");
    const bsOffcanvas = new bootstrap.Offcanvas(offcanvasElement);
    bsOffcanvas.show();
  }, []);


  return (
    <div className="">
      <hr className="mt-0" />
      <div
        className="offcanvas offcanvas-start"
        data-bs-scroll="true"
        data-bs-backdrop="false"
        tabIndex="-1"
        id="offcanvasScrolling3"
        aria-labelledby="offcanvasScrollingLabel"
        style={{
          top: `${navbarHeight}px`,
          height: `calc(100vh - ${navbarHeight}px)`,
          width: "17%", 
          borderTop: "1px solid lightgray",
        }}
      >
        <Link
          to="/private"
          className="d-flex align-items-center mb-3 mb-md-0 me-0 link-dark text-decoration-none justify-content-center"
        ></Link>
        <ul className="nav nav-pills flex-column mb-auto mt-4 text-start me">
          <li className="nav-item mt-4 mb-4 ms-2">
            <Link
              id="discover"
              to={"/private"}
              className={style === "discover" ? "selected" : ""}
              onClick={() => {
                console.log("Clicked on discover");
                if (style !== "discover") setStyle("discover");
              }}
            >
              <strong>
                <i className="fa-solid fa-heart-circle-plus"></i>Discover
              </strong>
            </Link>
          </li>
          <li className="nav-item mt-2 mb-4 ms-2">
            <Link
              id="messages"
              to={"/messages"}
              className={style === "messages" ? "selected" : ""}
              onClick={() => {
                console.log("clicked on messages");
                if (style !== "messages") setStyle("messages");
              }}
            >
              <strong>
                <i className="fa-solid fa-envelope"></i>Messages
              </strong>
            </Link>
          </li>
          <li className="nav-item mb-2">
            <Notifications style={style} setStyle={setStyle} />
          </li>
          <li className="nav-item mt-4 mb-4 ms-2">
            <Link
              id="profile-pill"
              to="/profile"
              className={style === "profile" ? "selected" : ""}
              onClick={() => {
                console.log("clicked on profile");
                if (style !== "profile") setStyle("profile");
              }}
            >
              <strong><i class="fa-solid fa-circle-user"></i>Profile</strong>
            </Link>
          </li>
          <li className="nav-item mt-2 mb-4 ms-2">
            <Link
              id="settings-pill"
              to="/settings"
              className={style === "settings" ? "selected" : ""}
              onClick={() => {
                console.log("clicked on settings");
                if (style !== "settings") setStyle("settings");
              }}
            >
              <strong><i class="fa-solid fa-gear"></i>Settings</strong>
            </Link>
          </li>
        </ul>
        <hr />
        <div className="dropdown">
          <Link
            to="#"
            className="d-flex align-items-center link-dark text-decoration-none dropdown-toggle"
            id="dropdownUser2"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <img
              src={img}
              alt=""
              width="72"
              height="72"
              className="rounded-circle me-2 p-2"
            />
            <strong style={{ fontSize: "15px" }}>UserName</strong>
          </Link>
          <ul
            className="dropdown-menu text-small shadow"
            aria-labelledby="dropdownUser2"
          >
            <li>
            </li>
            <li>
              <Link
                onClick={() => actions.logout()}
                className="dropdown-item"
                to="#"
              >
                Sign out
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
