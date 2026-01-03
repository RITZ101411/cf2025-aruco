export type User = {
  session_id: string;
  display_name: string | null;
  balance: number;
  total_plays: number;
  total_balance: number;
  user_id: number;
};


export type RankingUser = {
  name: string;
  point: number;
};