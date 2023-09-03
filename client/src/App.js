import './App.scss';
import { Pages } from './routes/routes';
import Header from './components/Header/Header'

function App() {
  return (
    <div className="App">
      <Header />
      <Pages />
    </div>
  );
}

export default App;
