import React from "react";
import styles from "./Home.module.css";

const ranking = [
  { name: "HogeHoge", point: 13498 },
  { name: "FugaFuga", point: 6668 },
  { name: "PiyoPiyo", point: 6668 },
];

export default function Home() {
  return (
    <div className={styles.root}>
      <div className={styles.background}>
        <div className={styles.topPanel}>
          <div className={styles.marker}>
            <img src="/images/marker.svg" alt="marker" />
          </div>
          <div className={styles.balanceCard}>
            <span className={styles.balanceLabel}>残高</span>
            <span className={styles.balanceValue}>0</span>
            <span className={styles.balanceUnit}>Pt</span>
          </div>
        </div>
        <div className={styles.cards}>
          <div className={styles.profile}>
            <div className={styles.profileName}>田中太郎さん</div>
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
            {ranking.map((r, i) => (
              <div className={styles.rankingRow} key={r.name}>
                <span className={styles.rankingLabel}>
                  {i + 1}. {r.name}
                </span>
                <span className={styles.rankingValue}>{r.point}Pt</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}