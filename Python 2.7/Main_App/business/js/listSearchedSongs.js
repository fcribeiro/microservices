let Song = function(props) {
    return (
        <tr>
                <td>{props.title}</td>
                <td>{props.artist}</td>
                <td>{props.album}</td>
                <td>{props.release_year}</td>
                <td><a key={props.id} href={'/addSongPlayList?sID='+props.id} className="btn btn-warning"><span className="glyphicon glyphicon-music"></span></a></td>
        </tr>
    )

}

let ShowSongs = React.createClass({

    getInitialState: function() {
        return {
            songs: []
        }
    },

    componentDidMount: function() {
        axios.get("/getSongsCriteria").then(results =>{
            console.log(results.data)
            this.setState({
                songs: results.data

            })
        })

    },

    render: function() {

        return (

            <div>
                <div className="container">
    <h2>Songs</h2>
    <table className="table table-hover">
        <thead>
        <tr>
            <th>Title</th>
            <th>Artist</th>
            <th>Album</th>
            <th>Release Year</th>
            <th>Add To Playlist</th>
        </tr>
        </thead>

        <tbody>
            {this.state.songs.map(function(song){
                return <Song title={song["title"]} artist={song["artist"]} album={song["album"]} release_year={song["release_year"]} id={song["id"]} key={song["id"]}/>
            })}
        </tbody>

    </table>
</div>
            </div>
        )
    }

})


ReactDOM.render(<ShowSongs/>, mountNode);

