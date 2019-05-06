import React, { Component } from 'react';
import logo from './logo.svg';
import './index3.css';

class App extends Component {
  render() {
    return (
		<div className="overlay">
			<form action="/checkout" method="post">
			<div className="d-a-t-a-a-g-o-r-a">
				
				<img id="shark2" src="{{ url_for('static', filename='images/shark.png') }}" alt="" />
				D A T A A G O R A
				<img id = "shark" src="{{ url_for('static', filename='images/shark.png') }}" alt="" />
				
					<input type="image" id="cart" src="{{ url_for('static', filename='images/cart.png') }}" alt="" />
				
			</div>
			</form>
			<br/> <br/> <br/> <br/> <br/>
			<form id="myForm" action="/results" method="post">
			<div class = "insta rectangle">
				<div class = "testo">
					<input className="icon" name = "categ" id="inst" type="image" value = "Fitbit" src="{{ url_for('static', filename='images/fitbit.png') }}" />
					<div class = "vertical">Fitbit</div>
				</div>
				<div class = "testo">
					<input className="icon" name = "categ"id="inst" type="image" value = "Fitbit"src="{{ url_for('static', filename='images/instagram.png') }}" />
					<div className="vertical">Instagram</div>
				</div>
				<div className="testo">
					<input className="icon" name = "test"id="inst" type="image" value = "Uber"src="{{ url_for('static', filename='images/fb.png') }}" />
					<div className="vertical">Facebook</div>
				</div>
				<div className="testo">
					<input className="icon" name = "test"id="inst" type="image" value = "Twitter"src="{{ url_for('static', filename='images/twitter.png') }}" />
					<div className="vertical">Twitter</div>
				</div>
				<div className="testo">
					<input className="icon" name="categ" id="inst" type="image" value = "Fitbit"src="{{ url_for('static', filename='images/snap.png') }}" />
					<div className="vertical">Snapchat</div>
				</div>
			</div>
			<br/> <br/>
			<div className="insta rectangle"> 
				<div className="testo">
					<input className="icon" name = "categ"id="inst" type="image" value = "Fitbit"src="{{ url_for('static', filename='images/ln.png') }}" />
					<div className="vertical">LinkedIn</div>
				</div>
				<div className="testo">
					<input className="icon" name = "test"id="inst" type="image" value = "Lyft"src="{{ url_for('static', filename='images/Pint.gif') }}" />
					<div className="vertical">Pinterest</div>
				</div>
				<div className="testo">
					<input className="icon" name="categ" id="inst" type="image" value = "Fitbit"src="{{ url_for('static', filename='images/yelp.png') }}" />
					<div className="vertical">Yelp</div>
				</div>
				<div className="testo">
					<input className="icon" name="categ" id="inst" type="image" value = "Fitbit"src="{{ url_for('static', filename='images/locations.png') }}" />
					<div className="vertical">Google Maps</div>
				</div>
				<div className="testo">
					<input className="icon" name="categ" id="inst" type="image" value = "Fitbit"src="{{ url_for('static', filename='images/apple.png') }}" />
					<div className="vertical">Apple Health</div>
				</div>
			</div>
			<br/>
			<div className="insta rectangle">
				<div className="testo">
					<input className="icon" name="test" id="inst" type="image" value="Fitbit" src="{{ url_for('static', filename='images/amazon.png') }}" />
					<div className="vertical">Amazon</div>
				</div>
				<div className="testo">
					<input className="icon" name="categ" id="inst" type="image" value="Fitbit" src="{{ url_for('static', filename='images/wsup.png') }}" />
					<div className="vertical">WhatsApp</div>
				</div>
				<div className="testo">
					<input className="icon" name="test" id="inst" type="image" value="Spotify" src="{{ url_for('static', filename='images/spotify.png') }}" />
					<div className="vertical">Spotify</div>
				</div>
				<div className="testo">
					<input className="icon" name="categ" id="inst" type="image" value="Fitbit" src="{{ url_for('static', filename='images/reddit.png') }}" />
					<div className="vertical">Reddit</div>
				</div>
				<div className="testo">
					<input className="icon" name="categ" id="inst" type="image" value="Fitbit" src="{{ url_for('static', filename='images/venmo.png') }}" />
					<div className="vertical">Venmo</div>
				</div>
			</div>
			</form>
		</div>
		
    );
  }
}

export default App;
