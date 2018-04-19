var col = JSON.parse('{{cols|safe}}');
var maxUsers = '{{users}}';
console.log("hi there");
//var place = this.refs.current;
var us = 50;
var baros = [
    [62, 126, 89, 79, 32],
    [83, 22, 49, 130, 126],
    [39, 90, 73, 126, 67],
    [126, 48, 96, 18, 33]
]

function changeClass(ido) {
    console.log(ido);
    if (ido.className === "coloo") {
        ido.className = "coloo2";
    } else {
        ido.className = "coloo";
    }

}
function tick() {
    var test = document.getElementById('us');
    if (test) {
        us = document.getElementById('us').value;
    }
    if (us > maxUsers) {
        us = maxUsers;
    }
    ReactDOM.render(React.createClass({ render: function () { return (<div>{us}</div>) } }), this.refs.stuff);
}
//setInterval(tick, 10000);

var realPython = React.createClass({
    maxUsers: '{{users}}',
    setUsers: function (val) {
        this.refs.stuff.innerText = this.maxUsers;
    },
    updateUsers: function (evt) {
        this.setState({
            inputUsers: evt.target.value
        });
    },
    updateTime: function (evt) {
        this.setState({
            inputTime: evt.target.value
        });
    },
    updateAge: function (evt) {
        this.setState({
            inputAge: evt.target.value
        });
    },
    getInitialState: function () {
        return {
            inputUsers: 50,
            inputTime: 6,
            inputAge: 20,
        };
    },
    handleChange: function (event) {
        this.setState({ value: event.target.value });
    },
    render: function () {
        return (<div className="overlay">
            <div className="d-a-t-a-a-g-o-r-a">
                <img id="shark2" src="{{ url_for('static', filename='images/shark.png') }}" alt="" /> D A T A A G O R A
            <img id="shark" src="{{ url_for('static', filename='images/shark.png') }}" alt="" />
            </div>
            <br />

            <div className="fitbit">
                <img className="icon2 align" src="{{ url_for('static', filename='images/fitbit.png') }}" alt="" /> F I T B I T
          </div>
            <div className="overall">
                <div className="rectangle7">

                    <div className="customize-search">
                        <span className="undo">
                            CUSTOMIZE SEARCH
                </span>
                    </div>
                    <br />
                    <div className="ovflow">
                        <div className="bel">
                            <div className="budget">
                                USERS
                        </div>
                            <div className="slido">
                                <span className="lab">10</span>
                                <input id="us" type="range" min="10" max="200" value={this.state.inputUsers} onChange={this.updateUsers} />
                                <span className="lab">200</span>
                            </div>
                            <div className="verticalo bel" id="use">{this.state.inputUsers}</div>
                        </div>
                        <div className="bel">
                            <div className="budget">
                                DURATION
                        </div>
                            <div className="slido">
                                <span className="lab">1 mon</span>
                                <input id="dur" type="range" min="1" max="12" value={this.state.inputTime} onChange={this.updateTime} />
                                <span className="lab">12 mon</span>
                            </div>
                            <div className="verticalo bel" id="dura">{this.state.inputTime}</div>
                        </div>
                        <div className="bel">
                            <div className="budget">
                                AGES
                            </div>
                            <div className="slido">
                                <span className="lab">18</span>
                                <input id="ages" type="range" min="18" max="35" value={this.state.inputAge} onChange={this.updateAge} />
                                <span className="lab">35</span>
                            </div>
                            <div className="verticalo bel" id="agos">{this.state.inputAge}</div>
                        </div>
                    </div>
                    <br />

                    <div className="customize-search">
                        <span className="undo">
                            VARIABLES
                </span>
                    </div>
                    <br />
                    <div className="hullo">
                        <div id="stuff" ref='stuff' />
                    </div>


                </div>
                <div className="rectangle7">
                    <div className="customize-search">
                        <span className="undo">
                            YOUR RESULTS
                </span>
                    </div>
                    <br />
                    <div className="geo">
                        <span id="usero"></span>
                        <span id="budge">users</span>
                        <br />
                        <img className="mapo" src="{{ url_for('static', filename='images/map.png') }}" alt="" />
                        <br />
                    </div>

                    <div className="age-range">Age Range</div>
                    <div id="rangos" className="ranges"></div>
                    <div id="bars">
                        <div id="b1" className="bar1 bar"></div>
                        <div id="b2" className="bar2 bar"></div>
                        <div id="b3" className="bar3 bar"></div>
                        <div id="b4" className="bar4 bar"></div>
                        <div id="b5" className="bar5 bar"></div>
                    </div>
                    <br />
                    <div className="udumb">
                        <span className="total">TOTAL: </span>
                        <span id="moneys"></span>
                        <br />
                    </div>
                    <div className="udumb">
                        <form action="/execute" method="post">
                            <button className="add-to-bag" type="submit" name='download' value='fitbit'>DOWNLOAD</button>
                        </form>
                    </div>

                </div>
            </div>

        </div>);
    }
});
ReactDOM.render(
    React.createElement(realPython, null),
    document.getElementById('content')
);