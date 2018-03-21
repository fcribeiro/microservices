
let ShowSong = React.createClass({

    getInitialState: function() {
        return {
            song: []
        }
    },

    componentDidMount: function() {
        axios.get("/getSongInfo").then(results =>{
            console.log(results.data)
            this.setState({
                song: results.data

            })
        })

    },

    render: function() {

        return (

            <div className="container">
                <h2>Edit Song</h2>
                <form action="/mySongEdit" method="post">
                    <div className="form-group">
                        <label for="title">Title:</label>
                        <input type="text" className="form-control" id="title" name="title" placeholder={this.state.song['title']}></input>
                    </div>
                    <div className="form-group">
                        <label for="artist">Artist:</label>
                        <input type="text" className="form-control" id="artist" name="artist" placeholder={this.state.song['artist']}></input>
                    </div>
                    <div className="form-group">
                        <label for="album">Album:</label>
                        <input type="text" className="form-control" id="album" name="album" placeholder={this.state.song['album']}></input>
                    </div>
                    <div className="form-group">
                        <label for="release_year">Release Year:</label>
                        <input type="number" className="form-control" id="release_year" name="release_year" placeholder={this.state.song['release_year']} min="1500" max="2017"></input>
                    </div>
                        <input type="submit" className="btn btn-success btn-lg btn-block" name="editSongButton" value="Edit Song"/>
                </form>
            </div>
        )
    }

})


ReactDOM.render(<ShowSong/>, mountNode);

