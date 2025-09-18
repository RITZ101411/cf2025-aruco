import { useEffect, useState } from "react";
import styles from "./Home.module.css";
import type { User, RankingUser } from "../types/User";
import { getUsers, init } from "../api/apiClient";

export default function Home() {
  const [ranking, setRanking] = useState<RankingUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    const fetchRanking = async () => {
      try {
        const users = await getUsers();
        if (!Array.isArray(users)) throw new Error("ランキング取得に失敗しました");

        setRanking(
          users.map((u: User) => ({
            name: u.user_id ?? "NoName",
            point: u.balance ?? 0,
          }))
        );
      } catch (e: any) {
        setError(e?.message ?? "不明なエラーが発生しました");
        setRanking([]);
      } finally {
        setLoading(false);
      }
    };
    const initUser = async () => {
      try {
        const data = await init();
        setSessionId(data.session_id);
      } catch (error) {
        console.error("Init failed:", error);
      }
    };

    initUser();
    fetchRanking();
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
            <span className={styles.balanceValue}>0</span>
            <span className={styles.balanceUnit}>Pt</span>
          </div>
        </div>
        <div className={styles.cards}>
          <div className={styles.profile}>
            <div className={styles.profileName}>{sessionId}</div>
            <div className={styles.profileRow}>
              <span className={styles.profileLabel}>プレイ数</span>
              <span className={styles.profileValue}>34回</span>
            </div>
            <div className={styles.profileRow}>
              <span className={styles.profileLabel}>累計獲得Pt</span>
              <span className={styles.profileValue}>6666Pt</span>
            </div>
          </div>
          <div className={styles.ranking}>
            <div className={styles.rankingTitle}>ランキング</div>
            {loading ? (
              <div>読み込み中...</div>
            ) : error ? (
              <div style={{ color: 'red' }}>{error}</div>
            ) : ranking.length === 0 ? (
              <div>ランキングデータがありません</div>
            ) : (
              ranking.map((r, i) => (
                <div className={styles.rankingRow} key={r.name + i}>
                  <span className={styles.rankingLabel}>
                    {i + 1}. {r.name}
                  </span>
                  <span className={styles.rankingValue}>{r.point}Pt</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}