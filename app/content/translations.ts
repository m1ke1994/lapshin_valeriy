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
      filters: {
        domain: string
        stage: string
        searchLabel: string
        searchPlaceholder: string
        reset: string
        empty: string
        results: string
        all: string
      }
      cards: { title: string; body: string; meta: string; category?: string; stage?: string; tags?: string[] }[]
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
      submitSuccess: string
      submitError: string
      submitErrorFallback: string
      modalOk: string
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
      logoTagline: 'Инжиниринговое бюро',
      nav: ['Философия', 'Метод', 'Компетенции', 'Доверие', 'Проекты', 'Контакты'],
      cta: 'Назначить звонок',
      menuTitle: 'Навигация',
      menuClose: 'Закрыть меню',
      menuOpenLabel: 'Открыть меню',
      languageLabel: 'Сменить язык',
      languageShort: { ru: 'RU', en: 'EN' },
    },
    hero: {
      eyebrow: 'IKB — контрактное инженерное бюро и R&D',
      title: 'Проектируем и выводим инженерные продукты на рынок.',
      lead:
        'Закрываем весь цикл: формулировка задачи, архитектура продукта, механика и электроника, встроенное ПО, тесты и предпроизводственная подготовка. Работаем как единый инженерный стрим для B2B-команд — аккуратно, системно, с измеримыми результатами. NDA подписываем на входе и ведём проект в формате «единого окна».',
      ctas: { primary: 'Назначить звонок', secondary: 'Посмотреть проекты' },
      metrics: [
        { value: '18+ лет', label: 'инжиниринга и производства' },
        { value: '100+ изделий', label: 'прототипы, MVP и пилоты' },
        { value: 'NDA', label: 'конфиденциальность по умолчанию' },
      ],
      notes: [
        {
          title: 'Сложные системы под ключ',
          body:
            'Точная механика, силовая электроника, промышленная автоматизация, связь, FPGA/embedded, стенды и валидация. Решение подстраиваем под бизнес-задачу: надёжность, себестоимость, производимость, сроки.',
        },
        {
          title: 'Процесс, который держит слово',
          body:
            'Персональный PM, прозрачные артефакты (спеки, схемы, BOM, протоколы), учёт рисков на каждом цикле. Документация готова к аудиту, статусы понятны, «чёрных ящиков» нет.',
        },
      ],
    },
    values: {
      eyebrow: 'Философия IKB',
      title:
        'Инновация — конфиденциальность — безопасность. Так мы доводим идеи до серийного продукта: расчётливо, аккуратно, с полной документацией.',
      cards: [
        {
          title: 'Системная инженерия вместо угадываний',
          body:
            'Проектируем через модели: механика, электротермальные режимы, логика управления, отказоустойчивость. Вшиваем промышленную практику — интерфейсы и сценарии управления (RS-485/DALI, по времени/событию/датчикам), устойчивое питание и предсказуемость в поле.',
        },
        {
          title: 'Конфиденциальность и безопасность по умолчанию',
          body:
            'NDA ещё до старта. Внутри проекта ведём логи рисков и решений, чтобы не было сюрпризов на финише. Безопасность не лозунг: контроль нагрузок и температур, диагностика, fail-safe, понятные политики доступа.',
        },
        {
          title: 'Готовность к производству',
          body:
            'Передаём полный комплект: паспорта, инструкции, схемы, BOM, прошивки, протоколы испытаний. Поддерживаем пилот и предсерийку, настраиваем технологичность, стабильную сборку и качество партии, чтобы продукт можно было производить, обслуживать и масштабировать.',
        },
      ],
    },
    approach: {
      eyebrow: 'Метод',
      title: 'Работаем как одна команда: консалтинг, R&D и передача в производство.',
      lead: 'Каждый этап экономит время на стыках, держит качество и управляет рисками.',
      steps: [
        {
          title: 'Запуск и NDA',
          body: 'Подписываем NDA, фиксируем требования, проводим стратегическую сессию, определяем критерии успеха и стартовые артефакты.',
        },
        {
          title: 'Системная концепция',
          body: 'Анализ функций и стоимости, выбор технологий, оценка рисков и сроков, дорожная карта и модель ресурсов.',
        },
        {
          title: 'Проектирование и прототипы',
          body: 'CAD/CAE, силовая и слаботочная электроника, прошивки, быстрые стенды и 3D-печать, тестирование гипотез на лабораторных стендах.',
        },
        {
          title: 'Валидация и производство',
          body: 'Предсерийные образцы, планы испытаний, сопровождение сертификации, передача пакета в производство и запуск первой партии.',
        },
      ],
    },
    competencies: {
      eyebrow: 'Компетенции',
      title: 'Полный стек инженерных дисциплин в одном центре.',
      cards: [
        {
          title: 'Мехатроника и точная механика',
          body: 'Прецизионные приводы, кинематика, расчёты по теплу и прочности, компоновка в ограниченном габарите.',
        },
        {
          title: 'Электроника и прошивки',
          body:
            'Плотные платы, питание и датчики, RTOS/Embedded Linux, драйверы, алгоритмы безопасности и киберзащита.',
        },
        {
          title: 'Цифровое моделирование',
          body: 'CAD/CAE, мультифизика, CFD/FEM, расчёт ресурса и цифровые двойники для долговечности продукта.',
        },
        {
          title: 'Сертификация и качество',
          body:
            'ISO 9001/13485, IEC/EN, технические файлы, управление рисками, аудиты поставщиков и партнёры по производству.',
        },
      ],
    },
    trust: {
      eyebrow: 'Доверие',
      title: 'Работаем с лидерами индустрий и бережём тишину.',
      lead: 'Большая часть проектов под NDA. Ниже — как мы обеспечиваем качество и безопасность.',
      cards: [
        {
          title: 'Система качества',
          body:
            'Внутренняя система управления качеством на базе ISO 9001, процедуры и чек-листы под требовательные отрасли.',
        },
        {
          title: 'Готовность к MedTech',
          body:
            'Принципы ISO 13485 в работе: управление рисками, трассировка, подготовка техфайлов и протоколов.',
        },
        {
          title: 'Данные и NDA',
          body:
            'Закрытые периметры хранения, контроль доступа, шифрование и жёсткие NDA до любого обмена исходными данными.',
        },
        {
          title: 'Партнёры',
          body:
            'Сеть проверенных поставщиков и лабораторий для испытаний, сертификации и масштабирования продукта до серии.',
        },
      ],
    },
    projects: {
      eyebrow: 'Проекты',
      title: 'Доменная экспертиза и работающие внедрения.',
      lead: 'Часть портфеля под NDA. Ниже примеры архитектур и форматов сотрудничества.',
      filters: {
        domain: 'Домен',
        stage: 'Этап',
        searchLabel: 'Поиск',
        searchPlaceholder: 'Поиск по названию, описанию или тегам',
        reset: 'Сбросить',
        empty: 'Нет проектов под выбранные фильтры',
        results: 'Найдено',
        all: 'Все',
      },
      cards: [
        {
          title: 'Роботизированная линия контроля качества',
          body:
            'Высокоточная механика, машинное зрение и силовая электроника для непрерывной инспекции изделий без остановки линии.',
          meta: 'Автоиндустрия / 8 месяцев от концепции до пилота',
          category: 'Автопром',
          stage: 'Пилот',
          tags: ['машинное зрение', 'механика', 'силовая электроника'],
        },
        {
          title: 'Модуль медицинской визуализации',
          body:
            'Электроника, оптомеханика и прошивки, подготовка технических файлов и сопровождение лабораторных испытаний.',
          meta: 'MedTech / предсерийная партия',
          category: 'Медтех',
          stage: 'Предсерия',
          tags: ['оптомеханика', 'безопасность', 'прошивка'],
        },
        {
          title: 'Промышленный IoT-контроллер',
          body:
            'Устойчивость EMI/EMC, силовой каскад, драйверы датчиков, защищённые протоколы и цифровой двойник для полевых тестов.',
          meta: 'Промышленность / 60 000+ устройств в эксплуатации',
          category: 'Промышленный интернет вещей',
          stage: 'Серия',
          tags: ['интернет вещей', 'ЭМС', 'протоколы'],
        },
      ],
    },
    contacts: {
      eyebrow: 'Контакты',
      title: 'Назначим звонок в течение 48 часов.',
      lead: 'Заполните форму или напишите нам. NDA подписываем на входе, так что можно безопасно делиться материалами.',
      formTitle: 'Записаться на консультацию',
      fields: {
        name: { label: 'Имя', placeholder: 'Как к вам обращаться?' },
        phone: { label: 'Телефон', placeholder: '+7 (___) ___-__-__' },
        date: { label: 'Дата', placeholder: 'Выберите дату' },
        time: { label: 'Время', placeholder: 'Укажите время' },
      },
      note: 'Мы защищаем ваши данные и используем их только для ответа на запрос.',
      button: 'Отправить заявку',
      alt: 'Или на почту:',
      mailSubject: 'Заявка на консультацию — IKB',
      mailLabels: { name: 'Имя', phone: 'Телефон', date: 'Дата', time: 'Время' },
      submitSuccess: 'Заявка отправлена. Ответим в течение 48 часов.',
      submitError: 'Не удалось отправить.',
      submitErrorFallback: 'Попробуйте ещё раз или напишите на почту.',
      modalOk: 'ОК',
    },
    certificates: {
      eyebrow: 'Аккредитации',
      title: 'Сертификаты и награды',
      lead: 'Отзывы, дипломы и подтверждения квалификации.',
      items: [
        { id: 'cerc1', src: '/certificates/cerc1.JPG', title: 'Рекомендательное письмо', subtitle: 'AstraZeneca / RU', type: 'review' },
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
      eyebrow: 'IKB — contract engineering & R&D',
      title: 'We design and ship engineered products to market.',
      lead:
        'We cover the full cycle: problem framing, product architecture, mechanics and electronics, embedded software, testing, and pre-production prep. We work as a single engineering lane for B2B teams — careful, system-driven, with measurable outcomes. NDA is signed upfront and we operate in a single-window format.',
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
            'We design through models: mechanics, electrical and thermal modes, control logic, fault tolerance. We embed industrial practice — interfaces and control scenarios (e.g. RS-485/DALI, time/event/sensor driven), stable power and predictable behaviour in the field.',
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
      filters: {
        domain: 'Domain',
        stage: 'Stage',
        searchLabel: 'Search',
        searchPlaceholder: 'Search title, description or tags',
        reset: 'Reset',
        empty: 'No projects for the selected filters',
        results: 'Found',
        all: 'All',
      },
      cards: [
        {
          title: 'Robotic quality inspection line',
          body:
            'High-precision mechanics, machine vision, and power electronics for continuous product inspection without stopping the line.',
          meta: 'Automotive / 8 months from concept to pilot',
          category: 'Automotive',
          stage: 'Pilot',
          tags: ['vision', 'motion', 'power'],
        },
        {
          title: 'Medical imaging module',
          body:
            'Electronics, optomechanics, and firmware design, technical files preparation, and lab test support.',
          meta: 'MedTech / pre-series batch',
          category: 'MedTech',
          stage: 'Pre-series',
          tags: ['opto', 'safety', 'firmware'],
        },
        {
          title: 'Industrial IoT controller',
          body:
            'EMI/EMC robustness, power stage, sensor drivers, secured protocols, and a digital twin for field testing.',
          meta: 'Industry / 60 000+ devices in operation',
          category: 'IoT',
          stage: 'Series',
          tags: ['iot', 'emc', 'protocols'],
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
        date: { label: 'Date', placeholder: 'Pick a date' },
        time: { label: 'Time', placeholder: 'Pick a time' },
      },
      note: 'We keep your data safe and use it only to respond to your request.',
      button: 'Send request',
      alt: 'Or email:',
      mailSubject: 'Consultation request — IKB',
      mailLabels: { name: 'Name', phone: 'Phone', date: 'Date', time: 'Time' },
      submitSuccess: 'Request sent. We will respond within 48 hours.',
      submitError: 'Could not send.',
      submitErrorFallback: 'Please try again or drop us an email.',
      modalOk: 'OK',
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
