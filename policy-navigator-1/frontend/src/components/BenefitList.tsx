import React from 'react';

interface Benefit {
  id: string;
  title: string;
  description: string;
}

interface BenefitListProps {
  benefits: Benefit[];
}

const BenefitList: React.FC<BenefitListProps> = ({ benefits }) => {
  return (
    <div className="benefit-list">
      <h2 className="text-lg font-bold">Available Benefits</h2>
      <ul>
        {benefits.map((benefit) => (
          <li key={benefit.id} className="benefit-item">
            <h3 className="font-semibold">{benefit.title}</h3>
            <p>{benefit.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BenefitList;