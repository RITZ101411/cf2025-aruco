export type User = {
  session_id: string;
  display_name: string | null;
  balance: number;
  total_plays: number;
};


export type RankingUser = {
  name: string;
  point: number;
};