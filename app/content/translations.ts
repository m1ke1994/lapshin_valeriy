export type Locale = 'ru' | 'en'
export type DocType = 'review' | 'diploma' | 'certificate'

export const translations: Record<
  Locale,
  {
    header: {
      logoTagline: string
      nav: string[]
      cta: string
      menuTitle: string
      menuClose: string
      menuOpenLabel: string
      languageLabel: string
      languageShort: { ru: string; en: string }
    }
    hero: {
      eyebrow: string
      title: string
      lead: string
      ctas: { primary: string; secondary: string }
      metrics: { value: string; label: string }[]
      notes: { title: string; body: string }[]
    }
    values: {
      eyebrow: string
      title: string
      cards: { title: string; body: string }[]
    }
    approach: {
      eyebrow: string
      title: string
      lead: string
      steps: { title: string; body: string }[]
    }
    competencies: {
      eyebrow: string
      title: string
      cards: { title: string; body: string }[]
    }
    trust: {
      eyebrow: string
      title: string
      lead: string
      cards: { title: string; body: string }[]
    }
    projects: {
      eyebrow: string
      title: string
      lead: string
      cards: { title: string; body: string; meta: string }[]
    }
    contacts: {
      eyebrow: string
      title: string
      lead: string
      formTitle: string
      fields: {
        name: { label: string; placeholder: string }
        phone: { label: string; placeholder: string }
        date: { label: string; placeholder: string }
        time: { label: string; placeholder: string }
      }
      note: string
      button: string
      alt: string
      mailSubject: string
      mailLabels: { name: string; phone: string; date: string; time: string }
    }
    certificates: {
      eyebrow: string
      title: string
      lead: string
      items: { id: string; src: string; title: string; subtitle: string; type: DocType }[]
      typeLabels: Record<DocType, string>
      actions: { close: string; prev: string; next: string }
    }
  }
> = {
  ru: {
    header: {
      logoTagline: 'Инженерное бюро',
      nav: ['Философия', 'Методика', 'Направления', 'Доверие', 'Проекты', 'Контакты'],
      cta: 'Консультация',
      menuTitle: 'Навигация',
      menuClose: 'Закрыть меню',
      menuOpenLabel: 'Открыть меню',
      languageLabel: 'Переключить язык',
      languageShort: { ru: 'РУ', en: 'EN' },
    },
    hero: {
      eyebrow: 'ИКБ · контрактная разработка и ОКР',
      title: 'Проектируем и доводим инженерные продукты до рынка.',
      lead:
        'Берём на себя полный цикл: постановка задачи, проектирование, механика и электроника, embedded-ПО, испытания и подготовка к предсерии. Работаем с B2B-командами как единый инженерный контур — аккуратно, системно и с измеримыми результатами. NDA подписываем на старте и ведём проект в режиме "одного окна".',
      ctas: { primary: 'Запланировать встречу', secondary: 'Посмотреть проекты' },
      metrics: [
        { value: '18+ лет', label: 'инженерной практики и производства' },
        { value: '100+ изделий', label: 'прототипы, MVP и внедрения' },
        { value: 'NDA', label: 'конфиденциальность по умолчанию' },
      ],
      notes: [
        {
          title: 'Сложные системы под ключ',
          body:
            'Прецизионная механика, силовая электроника, промышленная автоматика, коммуникации, FPGA/embedded, стенды и валидация. Собираем решение под бизнес-цель: надёжность, себестоимость, технологичность, сроки.',
        },
        {
          title: 'Процесс, который держит сроки',
          body:
            'Выделенный PM, прозрачные артефакты (спеки, схемы, BOM, протоколы испытаний), контроль рисков на каждом цикле. Готовность к аудиту, аккуратная документация и понятные статусы без магии.',
        },
      ],
    },
    values: {
      eyebrow: 'Философия ИКБ',
      title:
        'Инновационность — конфиденциальность — безопасность. Так мы превращаем идеи в серийные изделия: расчётно, аккуратно, с полной документацией.',
      cards: [
        {
          title: 'Системная инженерия вместо "соберём и посмотрим"',
          body:
            'Проектируем через модель: механика, электрические и тепловые режимы, логика управления, отказоустойчивость. Закладываем промышленную практику — интерфейсы и сценарии управления (например, RS-485/DALI, работа по времени/событию/датчикам), устойчивое питание и предсказуемое поведение устройства в реальной эксплуатации.',
        },
        {
          title: 'Конфиденциальность и безопасность — по умолчанию',
          body:
            'NDA — до передачи материалов. Внутри проекта ведём реестры рисков и решений, чтобы не было сюрпризов на финале. Для нас "безопасность" — не лозунг: это контроль нагрузок, температур и режимов работы, продуманная диагностика, сценарии предотвращения аварий и понятные правила доступа.',
        },
        {
          title: 'Результат в формате производства',
          body:
            'Передаём полный комплект КД/ЭД: паспорта, инструкции, схемы, спецификации (BOM), прошивки, протоколы испытаний. Сопровождаем пилот и предсерию, помогаем довести изделие до технологичности, стабильной сборки и качества партии — так, чтобы продукт можно было выпускать, обслуживать и масштабировать.',
        },
      ],
    },
    approach: {
      eyebrow: 'Методика',
      title: 'Работаем как интегрированная команда: консалтинг, R&D и вывод в серию в едином контуре.',
      lead: 'Каждый этап построен так, чтобы экономить время на стыках, держать качество и управлять рисками.',
      steps: [
        {
          title: 'Синхронизация и NDA',
          body:
            'Подписываем NDA, фиксируем требования, проводим стратегическую сессию, формируем критерии успеха и артефакты запуска.',
        },
        {
          title: 'Системный концепт',
          body:
            'Функционально-стоимостной анализ, выбор технологий, расчёт рисков и сроков, дорожная карта и ресурсная модель проекта.',
        },
        {
          title: 'Проектирование и прототипы',
          body:
            'CAD/CAE, силовая и слаботочная электроника, прошивки, быстрые макеты и 3D-печать, испытания гипотез на стендах.',
        },
        {
          title: 'Валидация и серия',
          body:
            'Предсерийные образцы, тест-планы, сопровождение сертификации, передача пакета на производство и ввод первой партии.',
        },
      ],
    },
    competencies: {
      eyebrow: 'Направления',
      title: 'Полный спектр инженерных компетенций в одном руководящем центре.',
      cards: [
        {
          title: 'Мехатроника и точные механизмы',
          body: 'Прецизионные приводы, кинематика, тепловые и прочностные расчёты, компоновка в ограниченных габаритах.',
        },
        {
          title: 'Электроника и прошивки',
          body:
            'Высокоплотные платы, силовая часть и сенсорика, RTOS/Embedded Linux, драйверы, защитные алгоритмы и кибербезопасность.',
        },
        {
          title: 'Цифровое моделирование',
          body: 'CAD/CAE, мультифизика, CFD/FEM, расчёт долговечности и цифровые близнецы для прогнозирования ресурса изделия.',
        },
        {
          title: 'Сертификация и качество',
          body:
            'ISO 9001/13485, IEC/EN, подготовка технических файлов, управление рисками, аудит поставщиков и производственных партнёров.',
        },
      ],
    },
    trust: {
      eyebrow: 'Доверие',
      title: 'Работаем с лидерами отраслей и бережно храним их тишину.',
      lead: 'Большинство проектов под NDA. Показываем лишь часть инфраструктуры и подходов к контролю качества.',
      cards: [
        {
          title: 'Система качества',
          body:
            'Собственная система менеджмента качества, процедуры под ISO 9001 и чек-листы для сложных отраслевых стандартов.',
        },
        {
          title: 'Готовность к MedTech',
          body:
            'Работаем по принципам ISO 13485: риск-менеджмент, трассируемость, подготовка технических файлов и протоколов.',
        },
        {
          title: 'Данные и NDA',
          body:
            'Закрытые контуры хранения, контроль доступа, шифрование и юридически выверенные NDA до передачи исходных данных.',
        },
        {
          title: 'Партнёры',
          body:
            'Сеть сертифицированных поставщиков и лабораторий для испытаний, сертификации и вывода изделия в серию.',
        },
      ],
    },
    projects: {
      eyebrow: 'Проекты',
      title: 'Направления, в которых мы сильны и которые выводим на рынок.',
      lead: 'Часть портфеля закрыта NDA. Ниже — примеры архитектур и форматов сопровождения.',
      cards: [
        {
          title: 'Роботизированная линия контроля качества',
          body:
            'Система высокоточной механики, машинного зрения и силовой электроники для непрерывной проверки изделий без остановки линии.',
          meta: 'Автопром / 8 месяцев от концепта до пилота',
        },
        {
          title: 'Медицинский модуль визуализации',
          body:
            'Проектирование электроники, оптомеханики и прошивки, подготовка технических файлов, сопровождение лабораторных испытаний.',
          meta: 'MedTech / предсерийная партия',
        },
        {
          title: 'Индустриальный IoT-контроллер',
          body:
            'EMI/EMC-устойчивость, силовая часть, драйверы датчиков, защищённые протоколы, цифровой двойник для тестирования в поле.',
          meta: 'Промышленность / 60 000+ устройств в эксплуатации',
        },
      ],
    },
    contacts: {
      eyebrow: 'Контакты',
      title: 'Назначим звонок в течение 48 часов.',
      lead:
        'Заполните форму или напишите нам. NDA подписываем сразу, поэтому можно прислать контекст и материалы.',
      formTitle: 'Запланировать консультацию',
      fields: {
        name: { label: 'Имя', placeholder: 'Как к вам обращаться' },
        phone: { label: 'Телефон', placeholder: '+7 (___) ___-__-__' },
        date: { label: 'Дата', placeholder: '' },
        time: { label: 'Время', placeholder: '' },
      },
      note: 'Бережно храним данные и используем их только для связи по вашему запросу.',
      button: 'Отправить заявку',
      alt: 'Или напишите:',
      mailSubject: 'Заявка на консультацию IKB',
      mailLabels: { name: 'Имя', phone: 'Телефон', date: 'Дата', time: 'Время' },
    },
    certificates: {
      eyebrow: 'Сертификаты',
      title: 'Подтверждённая экспертиза',
      lead: 'Отзывы, дипломы и сертификаты, подтверждающие нашу работу.',
      items: [
        { id: 'cerc1', src: '/certificates/cerc1.JPG', title: 'Рекомендательное письмо', subtitle: 'AstraZeneca, Россия', type: 'review' },
        { id: 'cerc2', src: '/certificates/cerc2.JPG', title: 'Диплом', subtitle: 'SPS/IPC/DRIVES-2012 (Германия)', type: 'diploma' },
        { id: 'cerc3', src: '/certificates/cerc3.jpg', title: 'Диплом', subtitle: 'INTHUB 2022 — бронзовая медаль', type: 'diploma' },
        { id: 'cerc4', src: '/certificates/cerc4.JPG', title: 'Сертификат', subtitle: 'Сертификат соответствия (ГОСТ Р)', type: 'certificate' },
      ],
      typeLabels: { review: 'Отзыв', diploma: 'Диплом', certificate: 'Сертификат' },
      actions: { close: 'Закрыть', prev: 'Назад', next: 'Вперёд' },
    },
  },
  en: {
    header: {
      logoTagline: 'Engineering bureau',
      nav: ['Philosophy', 'Method', 'Capabilities', 'Trust', 'Projects', 'Contacts'],
      cta: 'Book a call',
      menuTitle: 'Navigation',
      menuClose: 'Close menu',
      menuOpenLabel: 'Open menu',
      languageLabel: 'Change language',
      languageShort: { ru: 'RU', en: 'EN' },
    },
    hero: {
      eyebrow: 'IKB · contract engineering & R&D',
      title: 'We design and ship engineered products to market.',
      lead:
        'We cover the full cycle: problem framing, product architecture, mechanics and electronics, embedded software, testing, and pre-production prep. We work as a single engineering lane for B2B teams—careful, system-driven, with measurable outcomes. NDA is signed upfront and we operate in a "single window" format.',
      ctas: { primary: 'Schedule a call', secondary: 'View projects' },
      metrics: [
        { value: '18+ years', label: 'of engineering practice and manufacturing' },
        { value: '100+ units', label: 'prototypes, MVPs and deployments' },
        { value: 'NDA', label: 'confidentiality by default' },
      ],
      notes: [
        {
          title: 'Complex systems end-to-end',
          body:
            'Precision mechanics, power electronics, industrial automation, communications, FPGA/embedded, rigs and validation. We tailor the solution to the business goal: reliability, cost, manufacturability, timelines.',
        },
        {
          title: 'A process that keeps promises',
          body:
            'Dedicated PM, transparent artifacts (specs, schematics, BOMs, test protocols), risk tracking each cycle. Audit-ready docs and clear statuses with no black boxes.',
        },
      ],
    },
    values: {
      eyebrow: 'IKB philosophy',
      title:
        'Innovation — confidentiality — safety. This is how we turn ideas into serial products: calculated, careful, with complete documentation.',
      cards: [
        {
          title: 'Systems engineering over guesswork',
          body:
            'We design through models: mechanics, electrical and thermal modes, control logic, fault tolerance. We embed industrial practice—interfaces and control scenarios (e.g. RS-485/DALI, time/event/sensor driven), stable power and predictable behaviour in the field.',
        },
        {
          title: 'Confidentiality and safety by default',
          body:
            'NDA before any materials. Inside the project we maintain risk and decision logs so there are no surprises at the end. Safety is not a slogan: load and temperature control, diagnostics, fail-safes, and clear access policies.',
        },
        {
          title: 'Production-ready delivery',
          body:
            'We hand over the full design pack: passports, manuals, schematics, BOMs, firmware, and test protocols. We support pilot and pre-series, tuning for manufacturability, stable assembly, and batch quality so the product can be produced, serviced, and scaled.',
        },
      ],
    },
    approach: {
      eyebrow: 'Method',
      title: 'We operate as one integrated team: consulting, R&D, and series handover.',
      lead: 'Each stage saves time on handoffs, keeps quality, and manages risk.',
      steps: [
        {
          title: 'Kickoff and NDA',
          body: 'Sign NDA, capture requirements, hold a strategy workshop, define success criteria and launch artifacts.',
        },
        {
          title: 'System concept',
          body: 'Function-cost analysis, technology choices, risk and schedule estimates, roadmap, and resource model.',
        },
        {
          title: 'Design and prototypes',
          body: 'CAD/CAE, power and low-voltage electronics, firmware, quick rigs and 3D prints, hypothesis testing on benches.',
        },
        {
          title: 'Validation and production',
          body: 'Pre-series samples, test plans, certification support, production package handover, and first batch launch.',
        },
      ],
    },
    competencies: {
      eyebrow: 'Capabilities',
      title: 'A full range of engineering skills in one lead center.',
      cards: [
        {
          title: 'Mechatronics and precision mechanics',
          body: 'Precision drives, kinematics, thermal and strength calculations, packaging in tight envelopes.',
        },
        {
          title: 'Electronics and firmware',
          body:
            'High-density boards, power and sensing, RTOS/Embedded Linux, drivers, safety algorithms, and cybersecurity.',
        },
        {
          title: 'Digital simulation',
          body: 'CAD/CAE, multiphysics, CFD/FEM, lifetime prediction and digital twins for product durability.',
        },
        {
          title: 'Certification and quality',
          body:
            'ISO 9001/13485, IEC/EN, technical files, risk management, supplier audits, and production partners.',
        },
      ],
    },
    trust: {
      eyebrow: 'Trust',
      title: 'We serve industry leaders and guard their silence.',
      lead: 'Most engagements are under NDA. Here is a glimpse of our quality and security infrastructure.',
      cards: [
        {
          title: 'Quality system',
          body:
            'Internal quality management system, ISO 9001-based procedures, and checklists for demanding industry standards.',
        },
        {
          title: 'MedTech ready',
          body:
            'ISO 13485 principles in action: risk management, traceability, preparation of technical files and protocols.',
        },
        {
          title: 'Data & NDA',
          body:
            'Closed storage perimeters, access control, encryption, and watertight NDAs before any source data is shared.',
        },
        {
          title: 'Partners',
          body:
            'Network of certified suppliers and labs for testing, certification, and scaling the product to series.',
        },
      ],
    },
    projects: {
      eyebrow: 'Projects',
      title: 'Domains where we are strong and ship to market.',
      lead: 'Part of the portfolio is under NDA. Below are example architectures and engagement formats.',
      cards: [
        {
          title: 'Robotic quality inspection line',
          body:
            'High-precision mechanics, machine vision, and power electronics for continuous product inspection without stopping the line.',
          meta: 'Automotive / 8 months from concept to pilot',
        },
        {
          title: 'Medical imaging module',
          body:
            'Electronics, optomechanics, and firmware design, technical files preparation, and lab test support.',
          meta: 'MedTech / pre-series batch',
        },
        {
          title: 'Industrial IoT controller',
          body:
            'EMI/EMC robustness, power stage, sensor drivers, secured protocols, and a digital twin for field testing.',
          meta: 'Industry / 60 000+ devices in operation',
        },
      ],
    },
    contacts: {
      eyebrow: 'Contacts',
      title: 'We will schedule a call within 48 hours.',
      lead: 'Fill out the form or email us. NDA is signed upfront, so you can share context and materials safely.',
      formTitle: 'Book a consultation',
      fields: {
        name: { label: 'Name', placeholder: 'How should we address you?' },
        phone: { label: 'Phone', placeholder: '+1 (___) ___-__-__' },
        date: { label: 'Date', placeholder: '' },
        time: { label: 'Time', placeholder: '' },
      },
      note: 'We keep your data safe and use it only to respond to your request.',
      button: 'Send request',
      alt: 'Or email:',
      mailSubject: 'Consultation request · IKB',
      mailLabels: { name: 'Name', phone: 'Phone', date: 'Date', time: 'Time' },
    },
    certificates: {
      eyebrow: 'Credentials',
      title: 'Certificates & Awards',
      lead: 'Testimonials, diplomas, and certificates that validate our work.',
      items: [
        { id: 'cerc1', src: '/certificates/cerc1.JPG', title: 'Reference letter', subtitle: 'AstraZeneca / RU', type: 'review' },
        { id: 'cerc2', src: '/certificates/cerc2.JPG', title: 'Diploma', subtitle: 'SPS/IPC/DRIVES-2012 (Germany)', type: 'diploma' },
        { id: 'cerc3', src: '/certificates/cerc3.jpg', title: 'Diploma', subtitle: 'INTHUB 2022 — Bronze Medal', type: 'diploma' },
        { id: 'cerc4', src: '/certificates/cerc4.JPG', title: 'Certificate', subtitle: 'Certificate of conformity (GOST R)', type: 'certificate' },
      ],
      typeLabels: { review: 'Review', diploma: 'Diploma', certificate: 'Certificate' },
      actions: { close: 'Close', prev: 'Previous', next: 'Next' },
    },
  },
}
