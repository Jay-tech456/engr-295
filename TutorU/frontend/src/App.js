
import './App.css';
import LandingPage from "./Components/landingPage/landingPage"
import Chatbot from './Components/chatbot/chatbot';
import Team from './Components/Team/team';
function App() {
  return (
    <div className="App">
      <LandingPage />
      <Chatbot />
      <Team />
    </div>
  );
}

export default App;
