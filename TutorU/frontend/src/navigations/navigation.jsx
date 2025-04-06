// Components/Navigation/Navigation.js
import { NavLink, Link, useLocation } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import logo from "../artifact/Logo.gif";

function Navigation() {
  const [showMenu, setShowMenu] = useState(false);
  const [isHome, setIsHome] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setIsHome(location.pathname === "/");
  }, [location]);

  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  return (
    <div className="navigation">
      <div className="bigscreen">
        <div className="left">
          <p style={{ color: 'black'}}>PENCE CHHAY</p>
        </div>
        <div className="mid"></div>
        <div className="right" style={{ color: isHome ? 'white' : 'black' }}>
          <NavLink exact to="/" activeClassName="active" style={{ color: isHome ? 'white' : 'black' }}>Home</NavLink>
          <NavLink to="/chatbot" activeClassName="active" style={{ color: isHome ? 'white' : 'black' }}>Chatbot</NavLink>
          <NavLink to="/team" activeClassName="active" style={{ color: isHome ? 'white' : 'black' }}>Team</NavLink>
        </div>
      </div>
      <div className="mobilescreen">
        <div className="smallscreen">
          <div className="left">
            <p style={{ color: isHome ? 'white' : 'black' }}>PENCE CHHAY</p>
          </div>
          <div className="burger" onClick={toggleMenu}>
            <div className="bar"></div>
            <div className="bar"></div>
            <div className="bar"></div>
          </div>
        </div>
      </div>
      <div className={`menu ${showMenu ? 'open' : ''}`} onClick={toggleMenu}>
        <NavLink exact to="/" activeClassName="active">Home</NavLink>
        <NavLink to="/chatbot" activeClassName="active">Chatbot</NavLink>
        <NavLink to="/team" activeClassName="active">Team</NavLink>
      </div>
    </div>
  );
}

export default Navigation;