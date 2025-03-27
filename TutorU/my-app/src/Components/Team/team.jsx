import React from "react";
import "../../style/Team.css";
import teamMembers from "../../Hooks/team";

const Team = () => {
  return (
    <section className="team-section">
      <h1>Introducing Our Team Committed to Supporting MentorMind</h1>
      <div className="team-container">
        {teamMembers.map((member, index) => (
          <div className="team-member" key={index}>
            <img src={member.image} alt={member.name} className="profile-pic" />
            <h3>{member.name}</h3>
            <p className="position">{member.position}</p>
            {/* <p className="description">{member.description}</p> */}
          </div>
        ))}
      </div>
    </section>
  );
};

export default Team;
