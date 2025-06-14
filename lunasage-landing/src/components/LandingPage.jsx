// src/components/LandingPage.jsx
import React, { useEffect } from 'react';
import './LandingPage.css';
import AOS from 'aos';
import 'aos/dist/aos.css';
import moon from '../assets/moon.png';
import astronaut from '../assets/astronaut.png';
import earth from '../assets/planets/earth.png';
import mars from '../assets/planets/mars.png';
import jupiter from '../assets/planets/jupiter.png';
import saturn from '../assets/planets/saturn.png';
import neptune from '../assets/planets/neptune.png';
import uranus from '../assets/planets/uranus.png';
import venus from '../assets/planets/venus.png';
import mercury from '../assets/planets/mercury.png';
import spaceStation from '../assets/international-space-station.png';


const LandingPage = () => {
  useEffect(() => {
    AOS.init({ duration: 1500 });
  }, []);

  return (
    <div className="landing-container">
      <img src={moon} className="moon" alt="Moon" />
      <img src={astronaut} className="astronaut" alt="Astronaut" />
      <img src={earth} className="planet earth" alt="Earth" />
      <img src={mars} className="planet mars" alt="Mars" />
      <img src={jupiter} className="planet jupiter" alt="Jupiter" />
    <img src={saturn} className="planet saturn" alt="Saturn" />
    <img src={neptune} className="planet neptune" alt="Neptune" />
    <img src={uranus} className="planet uranus" alt="Uranus" />
    <img src={venus} className="planet venus" alt="Venus" />
    <img src={mercury} className="planet mercury" alt="Mercury" />
    <img src={spaceStation} className="international-space-station" alt="International Space Station" />


      <div className="content" data-aos="fade-up">
        <h1>LunaSage</h1>
        <p>Track lunar cycles for agriculture and astronomy.</p>
        <button className="cta-btn" data-aos="zoom-in">Explore Now</button>
      </div>
    </div>
  );
};

export default LandingPage;
