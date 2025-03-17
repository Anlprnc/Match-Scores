interface Match {
  away_score?: string;
  away_team: string;
  home_score?: string;
  home_team: string;
  minute?: string;
  stadium: string;
  status: string;
  kickoff?: string;
  home_logo?: string;
  away_logo?: string;
}

async function getMatches() {
  const res = await fetch('http://127.0.0.1:5000/matches');
  const data = await res.json();
  return data.data as Match[];
}

export default async function Home() {
  const matches = await getMatches();

  return (
    <div className="p-4 container mx-auto overflow-hidden">
      <h1 className="text-2xl font-bold mb-4">Matches</h1>
      <div className="grid gap-4">
        {matches.map((match, index) => (
          <div key={index} className="border p-4 rounded-lg">
            <div className="flex justify-between items-center px-1 md:px-10">
              <div className="w-[30%] flex justify-between items-center">
                <div className="flex items-center gap-2">
                  {match.home_logo && <img src={match.home_logo} alt={match.home_team} className="w-12 h-12 object-contain" />}
                  <p className="text-xl font-bold">{match.home_team}</p>
                </div>
                <p className="text-2xl font-bold text-center">{match.home_score || '-'}</p>
              </div>
              <div className="mx-4 text-center">
                <p className="text-sm">{match.status}</p>
                {match.minute && <p className="text-lg font-bold">{match.minute}</p>}
                {match.kickoff && <p className="text-lg">{match.kickoff}</p>}
                <p className="text-sm text-gray-500 mt-2 text-center">{match.stadium}</p>
              </div>
              <div className="w-[30%] flex gap-20 justify-between items-center">
                <p className="text-2xl font-bold text-center">{match.away_score || '-'}</p>
                <div className="flex items-center gap-2">
                  <p className="text-xl font-bold">{match.away_team}</p>
                  {match.away_logo && <img src={match.away_logo} alt={match.away_team} className="w-12 h-12 object-contain" />}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
