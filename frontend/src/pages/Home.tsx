import { useEffect, useState } from "react";
import styles from "./Home.module.css";
import type { User, RankingUser } from "../types/User";
import { getUsers, init as initUser } from "../api/apiClient";

export default function Home() {
  const [ranking, setRanking] = useState<RankingUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [session_id, setSessionId] = useState<string | null>(null);
  const [displayName, setDisplayName] = useState<string>("NoName");
  const [totalPlays, setTotalPlays] = useState<number>(0);
  const [balance, setBalance] = useState<number>(0);

  useEffect(() => {
    const initAndFetch = async () => {
      try {
        // ユーザー初期化 & ユーザー情報取得
        const data = await initUser();
        setSessionId(data.session_id);
        setDisplayName(data.display_name ?? "NoName");
        setBalance(data.balance ?? 0);
        setTotalPlays(data.total_plays ?? 0);

        // ランキング取得
        const users = await getUsers();
        if (!Array.isArray(users)) throw new Error("ランキング取得に失敗しました");

        setRanking(
          users.map((u: User) => ({
            name: u.display_name ?? "NoName",
            point: u.balance ?? 0,
          }))
        );
      } catch (e: any) {
        console.error("Init failed:", e);
        setError(e?.message ?? "不明なエラーが発生しました");
        setRanking([]);
      } finally {
        setLoading(false);
      }
    };

    initAndFetch();
  }, []);

  return (
    <div className={styles.root}>
      <div className={styles.background}>
        <div className={styles.topPanel}>
          <div className={styles.marker}>
            <img src="/src/assets/images/marker/marker.png" alt="marker" />
          </div>
          <div className={styles.balanceCard}>
            <span className={styles.balanceLabel}>残高</span>
            <span className={styles.balanceValue}>{balance}</span>
            <span className={styles.balanceUnit}>Pt</span>
          </div>
        </div>
        <div className={styles.cards}>
          <div className={styles.profile}>
            <div className={styles.profileName}>{displayName}</div>
            <div className={styles.profileRow}>
              <span className={styles.profileLabel}>プレイ数</span>
              <span className={styles.profileValue}>{totalPlays} 回</span>
            </div>
            <div className={styles.profileRow}>
              <span className={styles.profileLabel}>累計獲得Pt</span>
              <span className={styles.profileValue}>{balance} Pt</span>
            </div>
          </div>
          <div className={styles.ranking}>
            <div className={styles.rankingTitle}>ランキング</div>
            {loading ? (
              <div>読み込み中...</div>
            ) : error ? (
              <div style={{ color: "red" }}>{error}</div>
            ) : ranking.length === 0 ? (
              <div>ランキングデータがありません</div>
            ) : (
              ranking.map((r, i) => (
                <div className={styles.rankingRow} key={r.name + i}>
                  <span className={styles.rankingLabel}>
                    {i + 1}. {r.name}
                  </span>
                  <span className={styles.rankingValue}>{r.point} Pt</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
