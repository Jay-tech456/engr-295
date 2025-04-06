import React from 'react';
import '../../style/landingPage.css';
import landingPageImage from "../../artifacts/landingPageImage.png";

const LandingPage = () => {
    return (
        <div className="landing-container">
            <header className="header">
                <div className="logo">MENTORMIND</div>
                <nav className="nav-links">
                    <a href="#home">HOME</a>
                    <a href="#demo">DEMO</a>
                    <a href="#team">TEAM</a>
                    <a href="#contact">CONTACT</a>
                </nav>
            </header>

            <main className="main-content">
                <div className="image-section">
                    <img src={landingPageImage} alt="AI Learning" />
                </div>

                <div className="text-section">
                    <h1>Unlock the Future of <br / >Learning, Infinite <br /> Intelligence!</h1>
                    <p>Discover how AI is transforming education, making learning limitless and smarter than ever before.</p>

                    {/* "Learn More" link replacing the button */}
                    <a href="/learn-more" className="learn-more-link">Learn More →</a>
                </div>
            </main>
        </div>
    );
};

export default LandingPage;
