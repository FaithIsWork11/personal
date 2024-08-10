import React from "react";
import girlwithdog from "../../img/girlanddog2.jpg";
import ProfileInfo from "./profilecardinfo.jsx";

const ProfileCard = () => {
  return (
    <div className="profile-card mb-4">
      <img src={girlwithdog} className="card-img" />
        <h2 className="names" >Shaggy</h2>
        <h5 className="sub-name">& Kelsey</h5>
        <h6 className="breed-pill">Breed</h6>
        <h6 className="dog-age-pill">12</h6>
      <div className="justify-content-center d-flex">
        <i
          id="close"
          className="fa regular fa-circle-xmark"
          style={{ fontSize: "50px" }}
        ></i>
        <i
          id="reverse"
          className="fa regular fa-circle-left"
          style={{ fontSize: "50px" }}
        ></i>
        <i
          id="like"
          className="fa regular fa-circle-check"
          style={{ fontSize: "50px" }}
        ></i>
        <ProfileInfo />
      </div>
    </div>
  );
};

export default ProfileCard;
