let Song = function(props) {
    return (
        <tr>
                <td>{props.title}</td>
                <td>{props.artist}</td>
                <td>{props.album}</td>
                <td>{props.release_year}</td>
                <td><a key={props.id} href={'/mySongDelete?idSong='+props.id} className="btn btn-danger"><span className="glyphicon glyphicon-remove"></span></a></td>
        </tr>
    )

}

let ShowSongsIn = React.createClass({

    getInitialState: function() {
        return {
            songs: []
        }
    },

    componentDidMount: function() {
        axios.get("/getPlaylistSongs").then(results =>{
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
    <h2>My Playlist Songs</h2>
    <table className="table table-hover">
        <thead>
        <tr>
            <th>Title</th>
            <th>Artist</th>
            <th>Album</th>
            <th>Release Year</th>
            <th>Delete</th>
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


ReactDOM.render(<ShowSongsIn/>, mountNode);
