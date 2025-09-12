import React from "react";
import marker from "../assets/images/aruco_0.png";
import styles from "./HomePage12.module.css";

const rankingData = [
  { rank: 1, name: "hogeh...", pt: 100045 },
  { rank: 2, name: "fugaf...", pt: 100045 },
  { rank: 3, name: "piyop...", pt: 100045 },
];

const Home: React.FC = () => (
  <div className={styles.container}>
    <div className={styles.frame}>
      <div className={styles.rectangle1}></div>
      <div className={styles.panel}></div>
      <img src={marker} alt="Marker" className={styles.marker} />
      <div className={styles.balance}>
        <div className={styles.balanceRect}></div>
        <span className={styles.balanceLabel}>残高</span>
        <span className={styles.balanceValue}>1000</span>
        <span className={styles.balancePt}>Pt</span>
      </div>
      <div className={styles.ranking}>
        <div className={styles.rankingTitle}>ランキング</div>
        <div className={styles.rankingElements}>
          {rankingData.map((item, i) => (
            <div className={styles.rankingItem} style={{ top: `${i * 62}px` }} key={item.rank}>
              <div className={styles.rankingEllipse}></div>
              <div className={styles.rankingNumber}>{item.rank}</div>
              <div className={styles.rankingBalance}>
                <div className={styles.rankingBalanceRect}></div>
                <span className={styles.rankingBalanceLabel}>{item.name}</span>
                <span className={styles.rankingBalanceValue}>{item.pt}</span>
                <span className={styles.rankingBalancePt}>Pt</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className={styles.profile}>
        <div className={styles.profilePanel}>
          <div className={styles.profilePanelRect}></div>
          <div className={styles.profileElements}>
            <div className={styles.profileTitle}>表示名</div>
            <div className={styles.profileTotalPt}>
              <span className={styles.profileTotalLabel}>累計獲得Pt</span>
              <span className={styles.profileTotalValue}>9998</span>
            </div>
            <div className={styles.profilePlayCount}>
              <span className={styles.profilePlayLabel}>プレイ数</span>
              <span className={styles.profilePlayValue}>999</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default Home;